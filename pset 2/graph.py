# 6.100B Problem Set 2 Fall 2022
# Graph Optimization
# Name:
# Collaborators:


# This file contains a set of data structures to represent the graphs
# that you will be using for this pset.

class Node():
    """Represents a node in the graph"""

    def __init__(self, name):
        """
        Initializes an instance of Node object.

        Parameters:
            name: object
                The name of the node.
        """
        self.name = str(name)

    def get_name(self):
        """
        Returns:
            str
                The name of the node.
        """
        return self.name

    def __str__(self):
        """
        This is the function that is called when print(node) is called.

        Returns:
            str
                Humanly readable reprsentation of the node.
        """
        return self.name

    def __repr__(self):
        """
        Formal string representation of the node.

        Returns:
            str
                The name of the node.
        """
        return self.name

    def __eq__(self, other):
        """
        This is function called when you use the "==" operator on nodes.

        Parameters:
            other: Node
                Node object to compare against.

        Returns:
            bool
                True if self == other, False otherwise.
        """
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """
        This is function called when you used the "!=" operator on nodes.

        Parameters:
            other: Node
                Node object to compare against.

        Returns:
            bool
                True if self != other, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns:
            int
                Hash of the node. This function is necessary so that Nodes can be
                used as keys in a dictionary, Nodes are immutable.
        """
        return self.name.__hash__()


# PROBLEM 1: Implement this class based on the given docstring.
class DirectedRoad():
    """Represents a road (edge) with a travel time (weight)"""

    def __init__(self, src_node, dest_node, travel_time, road_type, traffic_multiplier):
        """
        Initialize src_node, dest_node, travel_time, road_type, traffic_multiplier for the DirectedRoad class

        Parameters:
            src_node: Node
                The source node.
            dest_node: Node
                The destination node.
            travel_time: float
                The time travelled between the src and dest.
            road_type: str
                The type of road of the edge.
            traffic_multiplier: float
                How much to multiply travel_time in the case of traffic.
                The traffic multiplier will always be at least 1.
        """
        self._src_node = src_node
        self._dest_node = dest_node
        self._travel_time = travel_time
        self._road_type = road_type
        self._traffic_multiplier = traffic_multiplier


    def get_source_node(self):
        """
        Getter method for DirectedRoad.

        Returns:
            Node
                The source node.
        """
        return self._src_node

    def get_destination_node(self):
        """
        Getter method for DirectedRoad.

        Returns:
            Node
                The destination node.
        """
        return self._dest_node

    def get_road_type(self):
        """
        Getter method for DirectedRoad.

        Returns:
            str
                The road type of the road.
        """
        return self._road_type 

    def get_travel_time(self, has_traffic=False):
        """
        Gets the travel_time for this road. If there is traffic,
        - multiply the time it takes to travel on a road by its traffic multiplier.

        Parameter:
            has_traffic: bool
                True if there is traffic, False otherwise.

        Returns:
            float
                The time to travel from the source node to the destination node.
        """
        if has_traffic: 
            return (self._traffic_multiplier*self._travel_time)
        else:
            return self._travel_time

        
    def get_traffic_multiplier(self):
        """
        Getter method for DirectedRoad.

        Returns:
            float
                The traffic multiplier.
        """
        return self._traffic_multiplier

    def __str__(self):
        """
        Function that is called when print() is called on a DirectedRoad object.

        Returns:
            str
                With the format
                'src -> dest takes travel_time minute(s) via road_type road with traffic multiplier traffic_multiplier'

        Note: For the total time assume normal traffic conditions.
        """
        return self._src_node.get_name() + ' -> ' + self._dest_node.get_name() + ' takes ' + str(self._travel_time) + ' minute(s) via ' + self._road_type + ' road with traffic multiplier ' + str(self._traffic_multiplier)

    def __hash__(self):
        """
        Returns:
            int
                Hash of the road. This function is necessary so that DirectedRoads can be
                used as keys in a dictionary, DirectedRoads are immutable.
        """
        return self.__str__().__hash__()


# node = Node('A')
# node1 = Node('B')
# obj = DirectedRoad(node, node1, 20.0, 'highway', 4.4)
# print(obj)


# PROBLEM 1: Implement methods of this class based on the given docstring.
# DO NOT CHANGE THE FUNCTIONS THAT HAVE BEEN IMPLEMENTED FOR YOU.
class RoadMap():
    """Represents a road map -> a directed graph of Node and DirectedRoad objects"""

    def __init__(self):
        """
        Initalizes a new instance of RoadMap.
        """

        self.nodes = set()
        self.nodes_to_roads = {}  # must be a dictionary of Node -> list of roads starting at that node

    def __str__(self):
        """
        Function that is called when print() is called on a RoadMap object.

        Returns:
            str
                Representation of the RoadMap.
        """

        road_strs = []
        for roads in self.nodes_to_roads.values():
            for road in roads:
                road_strs.append(str(road))
        road_strs = sorted(road_strs)  # sort alphabetically
        return '\n'.join(road_strs)  # concat road_strs with "\n"s between them

    def get_all_nodes(self):
        """
        Returns:
            set of Node
                A COPY of all nodes in the RoadMap. Does not modify self.nodes.
        """
        return self.nodes.copy()

    def contains_node(self, node):
        """
        Parameter:
            node: Node, node to check

        Returns:
            bool
                True, if node is in the graph; False, otherwise.
        """
        return (node in self.nodes)

    def insert_node(self, node):
        """
        Adds a Node object to the RoadMap.
        Raises a ValueError if it is already in the graph.

        Parameter:
            node: Node
                Node to add.
        """
        if node in self.nodes:
            raise ValueError('Already in graph')
        
        self.nodes.add(node)
        self.nodes_to_roads[node] = []


        # be sure to insert node into both self.nodes and self.nodes_to_roads


    def insert_road(self, road):
        """
        Adds a DirectedRoad instance to the RoadMap.
        Raises a ValueError if either of the nodes associated with the road is not in the graph.

        Parameter:
            road: DirectedRoad
                Road to add.
        """
        #chekc if source node or end node are in saved nodes, if not -> return value error
        if road.get_source_node() not in self.nodes or road.get_destination_node() not in self.nodes:
            raise ValueError
    
        self.nodes_to_roads[road.get_source_node()].append(road)



    def get_reachable_roads_from_node(self, node, restricted_roads):
        """
        Gets the roads out of Node node, excluding roads whose types are in restricted_roads.

        Parameters:
            node: Node
                Find reachable roads out of this node.
            restricted_roads: list of str (types of roads)
                Road types that cannot be traveled on.

        Returns:
            list of DirectedRoad
                A new list of all the roads that start at given node, whose types are not in restricted_roads.
                Empty list if the node is not in the graph.
        """
        if node not in self.nodes:
            return []
        
        if restricted_roads == None:
            restricted_roads = []
        l = []
        for i in self.nodes_to_roads[node]:
            if i.get_road_type() not in restricted_roads:
                l.append(i)

        return l

    