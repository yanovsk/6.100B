# 6.100B Problem Set 2 Fall 2022
# Graph Optimization
# Name: Dima Yanovsky
# Collaborators:

# Problem Set 2
# =============
# Finding shortest paths to drive from home to work on a road network

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2.1: Designing your Graph
#
#   What do the graph's nodes represent in this problem? What
#   do the graph's edges represent? Where are the times
#   represented?
#
# Write your answer below as a comment:
# Nodes N1-N8 are like "pitstops" between Home(start node) N0 and Work(finish node) N9
# These pitstops are connected by roads (edges)
# Time are an attribures of the road(edge) which connects two nodes
# So time is weight in our graph

# PROBLEM 2.2: Implementing create_graph
def create_graph(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Travel time and traffic multiplier should be each cast to a float.

    Parameters:
        map_filename : str
            Name of the map file.

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            source_node destination_node travel_time road_type traffic_multiplier

        Note: hill road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              1/4 as long as uphill travel. The travel_time represents the time to travel
              from source to destination (uphill).

        e.g.
            N0 N1 10 highway 1
        This entry would become two directed roads; one from 'N0' to 'N1' on a highway with
        a weight of 10.0, and another road from 'N1' to 'N0' on a highway using the same weight.

        e.g.
            N2 N3 7 uphill 2
        This entry would become two directed roads; one from 'N2' to 'N3' on a hill road with
        a weight of 7.0, and another road from 'N3' to 'N2' on a hill road with a weight of 1.75.
        Note that the directed roads created should have both type 'hill', not 'uphill'!

    Returns:
        RoadMap
            A directed road map representing the given map.
    """
    big_list = []
    with open(map_filename, 'r') as f:
        for row in f:
            big_list.append(row.replace('\n', '').split(' '))

    roadmap = RoadMap()

    for road in big_list:
        if Node(road[0]) not in roadmap.get_all_nodes():
                roadmap.insert_node(Node(road[0]))
        if Node(road[1]) not in roadmap.get_all_nodes():
            roadmap.insert_node(Node(road[1]))

        if road[3] == 'uphill': 
            #uphill source to destination
            roadmap.insert_road(DirectedRoad(Node(road[0]), Node(road[1]), (float(road[2])), 'hill', float(road[4])))
            #downhill dest to scr
            roadmap.insert_road(DirectedRoad(Node(road[1]), Node(road[0]), (float(road[2]))/4, 'hill', float(road[4])))
        else:
            #from scr to dest
            roadmap.insert_road(DirectedRoad(Node(road[0]), Node(road[1]), float(road[2]), road[3], float(road[4])))
            #from dest to scr
            roadmap.insert_road(DirectedRoad(Node(road[1]), Node(road[0]), float(road[2]), road[3], float(road[4])))
    return roadmap


# PROBLEM 2.3: Testing create_graph
#
#   Go to the bottom of this file, look for the section under FOR PROBLEM 2.3,
#   and follow the instructions in the handout.


# PROBLEM 3: Finding the Shortest Path using Optimized Search Method

# Problem 3.1: Objective function
#
#   What is the objective function for this problem? What are the constraints?
#
# Answer: Objective function is to minimize weight(time travelled) between start and ending node
#Constraint: cannot pass on any roads from the types listed in restricted_roads
# 
# Also, time travelled for best path is less than time travelled for all other possible paths
#
#

# PROBLEM 3.2: Implement find_shortest_path
def find_shortest_path(roadmap, start, end, restricted_roads=None, has_traffic=False):
    """
    Finds the shortest path between start and end nodes on the road map,
    without using any restricted roads, following traffic conditions.
    If restricted_roads is None, assume there are no restricted roads.
    Use Dijkstra's algorithm.

    Parameters:
        roadmap: RoadMap
            The graph on which to carry out the search.
        start: Node
            Node at which to start.
        end: Node
            Node at which to end.
        restricted_roads: list of str or None
            Road Types not allowed on path. If None, all are roads allowed
        has_traffic: bool
            Flag to indicate whether to get shortest path during traffic or not.

    Returns:
        A two element tuple of the form (best_path, best_time).
            The first item is a list of Node, the shortest path from start to end.
            The second item is a float, the length (time traveled) of the best path.
        If there exists no path that satisfies constraints, then return None.
    """
    if start not in roadmap.get_all_nodes() or end not in roadmap.get_all_nodes():
        return None
    if start == end:
        return ([start], 0)  # Empty path with 0 travel time

    unvisited = roadmap.get_all_nodes()
    distance_to = {node: float('inf') for node in roadmap.get_all_nodes()}
    distance_to[start] = 0

    # Mark all nodes as having no predecessor yet (no path from start).
    predecessor = {node: None for node in roadmap.get_all_nodes()}

    while unvisited:
        curr = min(unvisited, key = lambda node: distance_to[node])
        unvisited.remove(curr)

        # Stop if the smallest distance was infinity, means everything else in the queue is unreachable.
        if distance_to[curr] == float('inf'):
            break
        if curr == end:
            break
        #update curr best path and time
        for neighbor in roadmap.get_reachable_roads_from_node(curr, restricted_roads):
            weight = neighbor.get_travel_time(has_traffic)
            alternative_path_dist = distance_to[curr] + weight
            if alternative_path_dist < distance_to[neighbor.get_destination_node()]:
                distance_to[neighbor.get_destination_node()] = alternative_path_dist
                predecessor[neighbor.get_destination_node()] = curr

    # There is no path to end if its predecessor is still None.
    if start != end and predecessor[end] == None:  
        return None
    #otherwise trace path from end to start by walking thru predecessors list
    best_path = []
    while curr:
        best_path.insert(0, curr)
        curr = predecessor[curr]
    return(best_path, distance_to[end])

        
# PROBLEM 4.1: Implement find_shortest_path_no_traffic
def find_shortest_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during conditions of no traffic.
    Assume there are no restricted roads.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        list of Node
            The shortest path from start to end in normal traffic.
        If there exists no path, then return None.
    """
    g = create_graph(filename)
    result = find_shortest_path(g, start, end)
    if result:
        return result[0]
    else:
        return None


# PROBLEM 4.2: Implement find_shortest_path_restricted
def find_shortest_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and hill roads cannot be used.
    Assume no traffic.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        list of Node
            The shortest path from start to end given the aforementioned conditions.
        If there exists no path that satisfies constraints, then return None.
    """
    g = create_graph(filename)
    result = find_shortest_path(g, start, end,restricted_roads=['local','hill'] )
    if result:
        return result[0]
    else:
        return None



# PROBLEM 4.3: Implement find_shortest_path_in_traffic_no_toll
def find_shortest_path_in_traffic_no_toll(filename, start, end):
    """
    Finds the shortest path from start to end when toll roads cannot be used and in traffic,
    i.e. when all roads' travel times are multiplied by their traffic multipliers.

    You must use find_shortest_path.

    Parameters:
        filename: str
            Name of the map file that contains the graph
        start: Node
            Node object at which to start.
        end: Node
            Node object at which to end.

    Returns:
        list of Node
            The shortest path from start to end given the aforementioned conditions.
        If there exists no path that satisfies the constraints, then return None.
    """
    g = create_graph(filename)
    result = find_shortest_path(g, start, end, restricted_roads=['toll'], has_traffic=True)
    if result:
        return result[0]
    else:
        return None



if __name__ == '__main__':

    # UNCOMMENT THE LINES BELOW TO DEBUG OR TO EXECUTE PROBLEM 2.3


    small_map = create_graph('./maps/small_map.txt')

    # # ------------------------------------------------------------------------
    # # FOR PROBLEM 2.3


    # # ------------------------------------------------------------------------

    start = Node('N0')
    end = Node('N2')
    restricted_roads = []
    print(find_shortest_path(small_map, start, end, restricted_roads))
