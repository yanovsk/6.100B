from ps2 import create_graph, find_shortest_path

from graph import Node


class GraphVisualizer():

    def __init__(self, map_path):

        self.road_map = create_graph(map_path)

        self.nodes = list(self.road_map.get_all_nodes())

        self.node_names = [node.get_name() for node in self.nodes]

        self.road_type_colors = {'highway': 'red', 'hill': 'green', 'local':'blue', 'collector':'black', 'toll':'yellow'}

        import matplotlib.patches as mpatches

        red_handle = mpatches.Patch(color='red', label='highway')

        blue_handle = mpatches.Patch(color='blue', label='local')

        green_handle = mpatches.Patch(color='green', label='hill')

        black_handle = mpatches.Patch(color='black', label='collector')

        yellow_handle = mpatches.Patch(color='yellow', label='toll')

        self.handles = [red_handle, blue_handle, green_handle, black_handle, yellow_handle]





    def plot_part2_pyvis(self):

        from pyvis.network import Network

        net = Network(directed = True)



        # Add Nodes to Graph in format integer_id : node_name

        net.add_nodes([i for i in range(len(self.nodes))], label=self.node_names)

        m = {self.node_names[i] : i for i in range(len(self.nodes))}

    

        # Add edges and weights

        for node in self.nodes:

            reachable_roads = self.road_map.get_reachable_roads_from_node(node, [])

            for road in reachable_roads:

                src = node.get_name()

                dest = road.get_destination_node().get_name()

                time = road.get_travel_time() # assume no traffic

                net.add_edge(m[src], m[dest], label=str(time))



        # To see Graph, the html file must be opened in browser

        net.show('ps2_part2_sandbox.html') 



    def plot_part2_networkx(self):

        import matplotlib.pyplot as plt

        import networkx as nx

        net = nx.MultiDiGraph()

    

        net.add_nodes_from(self.node_names)

    

        # Add edges and weights

        for node in self.nodes:

            reachable_roads = self.road_map.get_reachable_roads_from_node(node, [])

            for road in reachable_roads:

                src = node.get_name()

                dest = road.get_destination_node().get_name()

                time = road.get_travel_time() # assume no traffic

                net.add_edge(src, dest, label=str(time))

    

        # Display Graph

        pos = nx.spectral_layout(net)

        nx.draw_networkx_nodes(net, pos, node_color="red", node_size=200)

        nx.draw_networkx_edges(net, pos, arrows=True, arrowstyle="->", arrowsize=10, connectionstyle="arc3,rad=0.10", width=2)

        nx.draw_networkx_labels(net, pos, font_size=10, font_family="sans-serif")

        #edge_labels = nx.get_edge_attributes(net, "label")

        #nx.draw_networkx_edge_labels(net, pos, edge_labels)

        plt.ion()

        plt.show()



    def plot_part2_pydot(self):

        import matplotlib.pyplot as plt

        import networkx as nx

        import pylab

        import graphviz

        import pydot

        net = nx.MultiDiGraph()

        net.add_nodes_from(self.node_names)

    

        # Add edges and weights

        for node in self.nodes:

            reachable_roads = self.road_map.get_reachable_roads_from_node(node, [])

            for road in reachable_roads:

                src = node.get_name()

                dest = road.get_destination_node().get_name()

                time = road.get_travel_time() # assume no traffic

                color = self.road_type_colors[road.get_road_type()]

                

                net.add_edge(src, dest, label=str(time), color=color)



        pydot_graph = nx.drawing.nx_pydot.to_pydot(net)

        pydot_graph.write_png('ps2_part2_sandbox.png')

        im = pylab.imread('ps2_part2_sandbox.png')

        pylab.legend(bbox_to_anchor=(0, 1), handles=self.handles, loc='upper left', fontsize='xx-small')



        img = pylab.imshow(im)

        #TODO: remove file



    def plot_part3_dijkstra(self, start, end):

        import networkx as nx

        import matplotlib.pyplot as plt

        import pylab 

        net = nx.MultiDiGraph()

        net.add_nodes_from(self.node_names)

    

        # Add edges and weights

        for node in self.nodes:

            reachable_roads = self.road_map.get_reachable_roads_from_node(node, [])

            for road in reachable_roads:

                src = node.get_name()

                dest = road.get_destination_node().get_name()

                time = road.get_travel_time() # assume no traffic

                net.add_edge(src, dest, label=time, color='black')

        

        # Plot True Dijkstra Path

        true_path = nx.dijkstra_path(net, start, end, weight='label')

        for i, node in enumerate(true_path):

            net.nodes[node]['style'] = 'filled'

            net.nodes[node]['fillcolor'] = 'purple'

            if i + 1 < len(true_path):

                next_node = true_path[i + 1]

                net.edges[(node, next_node, 0)]['color'] = 'purple'

                net.edges[(node, next_node, 0)]['penwidth'] = '5'



        # Plot Student's "Optimal Path" over True path

        student_path = find_shortest_path(self.road_map, Node(start), Node(end), [])

        for i, node in enumerate(student_path[0]):

            net.nodes[node.get_name()]['style'] = 'filled'

            net.nodes[node.get_name()]['fillcolor'] = 'orange'

            if i + 1 < len(true_path):

                next_node = true_path[i + 1]

                net.edges[(node.get_name(), next_node, 0)]['color'] = 'orange'

                net.edges[(node.get_name(), next_node, 0)]['penwidth'] = '5'



        # Color Start and End nodes appropriately

        net.nodes[start]['fillcolor'] = 'green'

        net.nodes[end]['fillcolor'] = 'red'

        

        # Relable edge labels as Strings (weird bug w/pydot on Spyder: 

        # throws error if edges are ints/floats)

        for src, dest, data in net.edges.data():

            data['label'] = str(data['label'])

        

        # Draw Graph

        pydot_graph = nx.drawing.nx_pydot.to_pydot(net)

        pydot_graph.write_png('ps2_part3_dijkstra_sandbox.png')

        im = pylab.imread('ps2_part3_dijkstra_sandbox.png')

        img = pylab.imshow(im)





if __name__ == '__main__':

    import sys

    args = sys.argv[1:]

    

    if args[0] == "2":

        map_path = args[1]

        grapher = GraphVisualizer(map_path)

        grapher.plot_part2_pydot()

    elif args[0] == "3":

        map_path, start, end = args[1:]

        grapher = GraphVisualizer(map_path)

        grapher.plot_part3_dijkstra(start, end)

