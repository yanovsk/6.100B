#!/usr/bin/env python

from graph import Node, DirectedRoad, RoadMap
from ps2 import create_graph, find_shortest_path, find_shortest_path_no_traffic, find_shortest_path_in_traffic_no_toll, find_shortest_path_restricted
import unittest

ROADMAP_FILENAME = "./maps/road_map.txt"
SMALLMAP_FILENAME = "./maps/small_map.txt"
HIGHWAY = "highway"
HILL = "hill"
LOCAL = "local"
TOLL = "toll"
COLLECTOR = "collector"


class InternalPs2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = RoadMap()
        cls.na = Node('NA')
        cls.nb = Node('NB')
        cls.nc = Node('NC')

        # for best path tests
        cls.n0 = Node('N0')
        cls.n1 = Node('N1')
        cls.n2 = Node('N2')
        cls.n3 = Node('N3')
        cls.n4 = Node('N4')
        cls.n5 = Node('N5')
        cls.n6 = Node('N6')
        cls.n7 = Node('N7')
        cls.n8 = Node('N8')
        cls.n9 = Node('N9')
        cls.n10 = Node('N10')

        cls.m.insert_node(cls.na)
        cls.m.insert_node(cls.nb)
        cls.m.insert_node(cls.nc)
        cls.r1 = DirectedRoad(cls.na, cls.nb, 5.0, 'local', 2.0)
        cls.r2 = DirectedRoad(cls.na, cls.nc, 10.0, 'hill', 1.0)
        cls.r3 = DirectedRoad(cls.nb, cls.nc, 18.0, 'highway', 1.0)
        cls.r4 = DirectedRoad(cls.n2, cls.n4, 1.75, 'hill', 1.0)

        cls.m.insert_road(cls.r1)
        cls.m.insert_road(cls.r2)
        cls.m.insert_road(cls.r3)

        try:
            cls.road_map = create_graph(ROADMAP_FILENAME)
            cls.small_map = create_graph(SMALLMAP_FILENAME)
        except NotImplementedError:
            cls.road_map = RoadMap()
            cls.small_map = RoadMap()

    # ------------------------------------------------ testing graph.py

    ## testing DirectedRoad
    def test_1_graph_weighted_edge_src(self):
        self.assertEqual(str(self.r1.get_source_node()), str(self.na), "your DirectedRoad get_source_node() method is failing.")
        self.assertEqual(str(self.r2.get_source_node()), str(self.na), "your DirectedRoad get_source_node() method is failing.")
        self.assertEqual(str(self.r3.get_source_node()), str(self.nb), "your DirectedRoad get_source_node() method is failing.")

    def test_1_graph_weighted_edge_dest(self):
        self.assertEqual(str(self.r1.get_destination_node()), str(self.nb), "your DirectedRoad get_destination_node() method is failing.")
        self.assertEqual(str(self.r2.get_destination_node()), str(self.nc), "your DirectedRoad get_destination_node() method is failing.")
        self.assertEqual(str(self.r3.get_destination_node()), str(self.nc), "your DirectedRoad get_destination_node() method is failing.")

    def test_1_graph_weighted_edge_type(self):
        self.assertEqual(self.r1.get_road_type(), 'local', "your DirectedRoad get_road_type() method is failing.")
        self.assertEqual(self.r2.get_road_type(), 'hill', "your DirectedRoad get_road_type() method is failing.")
        self.assertEqual(self.r3.get_road_type(), 'highway', "your DirectedRoad get_road_type() method is failing.")

    def test_1_graph_weighted_edge_total_time(self):
        self.assertEqual(self.r1.get_travel_time(), 5, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r2.get_travel_time(), 10, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r3.get_travel_time(), 18, "your DirectedRoad get_travel_time() method is failing, in no traffic.")
        self.assertEqual(self.r1.get_travel_time(has_traffic=True), 10, "your DirectedRoad get_travel_time() method is failing, in traffic for local road.")
        self.assertEqual(self.r2.get_travel_time(has_traffic=True), 10, "your DirectedRoad get_travel_time() method is failing, in traffic for hill road.")
        self.assertEqual(self.r3.get_travel_time(has_traffic=True), 18, "your DirectedRoad get_travel_time() method is failing, in traffic for highway road.")

    def test_1_graph_weighted_edge_traffic_multiplier(self):
        self.assertEqual(self.r1.get_traffic_multiplier(), 2.0, "your DirectedRoad get_traffic_multiplier() method is failing.")
        self.assertEqual(self.r2.get_traffic_multiplier(), 1.0, "your DirectedRoad get_traffic_multiplier() method is failing.")
        self.assertEqual(self.r3.get_traffic_multiplier(), 1.0, "your DirectedRoad get_traffic_multiplier() method is failing.")

    def test_1_graph_weighted_edge_str(self):
        self.assertEqual(str(self.r1), "NA -> NB takes 5.0 minute(s) via local road with traffic multiplier 2.0", "your DirectedRoad __str__() method is failing.")
        self.assertEqual(str(self.r2), "NA -> NC takes 10.0 minute(s) via hill road with traffic multiplier 1.0", "your DirectedRoad __str__() method is failing.")
        self.assertEqual(str(self.r3), "NB -> NC takes 18.0 minute(s) via highway road with traffic multiplier 1.0", "your DirectedRoad __str__() method is failing.")


    ## testing RoadMap
    def test_1_graph_insert_node(self):
        self.assertTrue(self.m.contains_node(self.nc), msg="Either your RoadMap insert_node() or contains_node() method are failing")

    def test_1_graph_insert_existing_node_raises(self):
        with self.assertRaises(ValueError, msg="your RoadMap insert_node() method doesn't raise ValueError when adding existing node to the map"):
            self.m.insert_node(self.na)

    def test_1_graph_get_all_nodes(self):
        expected_nodes = set([self.na,self.nb, self.nc])
        student_nodes_1 = self.m.get_all_nodes()
        self.assertEqual(student_nodes_1, expected_nodes, "Your RoadMap get_all_nodes() method doesn't return the correct nodes")
        # Check copy
        student_nodes_1.clear()
        student_nodes_2 = self.m.get_all_nodes()
        self.assertEqual(student_nodes_2, expected_nodes, "Your RoadMap get_all_nodes() method doesn't return the correct nodes a second time after mutating the output the first time")

    def test_1_graph_insert_road(self):
        self.assertEqual(self.m.get_reachable_roads_from_node(self.na, []), [self.r1, self.r2], "Your RoadMap get_reachable_roads_from_node() method doesn't return the correct roads")
        self.assertEqual(self.m.get_reachable_roads_from_node(self.n0, []),[], "Your RoadMap get_reachable_roads_from_node() method doesn't return [] when node is not in map")
        self.assertEqual(self.m.get_reachable_roads_from_node(self.na, [LOCAL]), [self.r2], "Your RoadMap get_reachable_roads_from_node() method doesn't return the correct roads when local roads are restricted")

    def test_1_graph_insert_road_to_nonexistent_node_raises(self):
        node_not_in_graph = Node('SC')
        no_src = DirectedRoad(self.nb, node_not_in_graph, 9, 'toll', 1)
        no_dest = DirectedRoad(node_not_in_graph, self.na, 9, 'toll', 1)

        with self.assertRaises(ValueError, msg="your RoadMap insert_road() method doesn't raise ValueError when adding road whose source is not in the map"):
            self.m.insert_road(no_src)
        with self.assertRaises(ValueError, msg="your RoadMap insert_road() method doesn't raise ValueError when adding road whose destination is not in the map"):
            self.m.insert_road(no_dest)

    def test_1_graph_str(self):
        lines = ["NA -> NB takes 5.0 minute(s) via local road with traffic multiplier 2.0",
                 "NA -> NC takes 10.0 minute(s) via hill road with traffic multiplier 1.0",
                 "NB -> NC takes 18.0 minute(s) via highway road with traffic multiplier 1.0"]
        actual = str(self.m).split("\n")
        self.assertIn(
            lines[0], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[1], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[2], actual, "Your printed graph does not match the correct string")

    # ------------------------------------------------ testing ps2.py

    def test_2_create_graph(self):
        self.assertIsInstance(self.road_map, RoadMap, f"Your create_graph() should have returned an instance of RoadMap, but instead returned an instance of {type(self.road_map)}.")
        self.assertEqual(len(self.road_map.nodes), 10, f"Your road map should have had 10 nodes, but instead had {len(self.road_map.nodes)} nodes.")
        all_roads = []
        for node, roads in self.road_map.nodes_to_roads.items():
            self.assertTrue(isinstance(node, Node), "A node in your road map is not of type Node")
            all_roads += roads  # edges must be dict of node -> list of edges
            for road in roads:
                self.assertTrue(isinstance(road, DirectedRoad), "A road in your roadmap is not of type DirectedRoad.")
                self.assertFalse('\n' in road.get_road_type(),
                                 "Your road type contains a new line character. Check the reading/parsing in create_graph")

        for node_number in range(10):
            self.assertTrue(Node("N" + str(node_number)) in self.road_map.get_all_nodes(), f"node {str(node_number)} is missing from your road map")

        # Check road bidirectionality
        all_roads = set(all_roads)
        for road in all_roads:
            road_start = road.get_source_node()
            road_end = road.get_destination_node()
            road_travel_time = road.get_travel_time()
            road_type = road.get_road_type()
            road_traffic_multiplier = road.get_traffic_multiplier()

            self.assertIsInstance(road_travel_time, float, f"For road {road}, expected the travel time {road_travel_time} to be a float, found it was a {type(road_travel_time)} instead.")
            self.assertIsInstance(road_traffic_multiplier, float, f"For road {road}, expected the traffic multiplier {road_traffic_multiplier} to be a float, found it was a {type(road_traffic_multiplier)} instead.")

            if road_type != 'hill':
                other_way_road = DirectedRoad(road_end, road_start, road_travel_time, road_type, road_traffic_multiplier)
                self.assertTrue(str(other_way_road) in str(self.road_map),
                              f"For non-hill road `{road}`, expected the road going the other way `{other_way_road}` be a road in your road map, but found it was not.")
            else:
                wrong_other_way_road = DirectedRoad(road_end, road_start, road_travel_time, road_type, road_traffic_multiplier)
                self.assertTrue(str(wrong_other_way_road) not in str(self.road_map),
                                 f"For hill road `{road}`, expected the road going the other way `{wrong_other_way_road}` NOT be a road in your road map, but found it was. Check you are dealing with uphill and downhill travel times correctly.")
                possible_other_way_road_1 = DirectedRoad(road_end, road_start, road_travel_time*4, road_type, road_traffic_multiplier)
                possible_other_way_road_2 = DirectedRoad(road_end, road_start, road_travel_time*1/4, road_type, road_traffic_multiplier)
                self.assertTrue((str(possible_other_way_road_1) in str(self.road_map)) or (str(possible_other_way_road_2) in str(self.road_map)),
                                f"For hill road `{road}`, expected either the road going the other way `{possible_other_way_road_1}` or `{possible_other_way_road_2}` be a road in your road map, but found neither was. Check you are dealing with uphill and downhill travel times correctly.")

        node0 = Node("N0")
        node1 = Node("N1")
        node2 = Node("N2")
        node3 = Node("N3")
        node4 = Node("N4")
        node5 = Node("N5")
        node6 = Node("N6")
        node7 = Node("N7")
        node8 = Node("N8")
        node9 = Node("N9")
        expected_roads = {
            DirectedRoad(node0, node1, 15.0, HIGHWAY, 2.0),
            DirectedRoad(node1, node0, 15.0, HIGHWAY, 2.0),
            DirectedRoad(node0, node2, 7.0, HILL, 1.0),
            DirectedRoad(node2, node0, 1.75, HILL, 1.0),
            DirectedRoad(node1, node3, 6.0, HIGHWAY, 3.0),
            DirectedRoad(node3, node1, 6.0, HIGHWAY, 3.0),
            DirectedRoad(node3, node2, 18.0, HILL, 1.0),
            DirectedRoad(node2, node3, 4.5, HILL, 1.0),
            DirectedRoad(node4, node2, 7.0, HILL, 1.0),
            DirectedRoad(node2, node4, 1.75, HILL, 1.0),
            DirectedRoad(node3, node6, 5.0, LOCAL, 4.0),
            DirectedRoad(node6, node3, 5.0, LOCAL, 4.0),
            DirectedRoad(node3, node8, 15.0, HIGHWAY, 1.0),
            DirectedRoad(node8, node3, 15.0, HIGHWAY, 1.0),
            DirectedRoad(node4, node5, 4.0, HIGHWAY, 2.0),
            DirectedRoad(node5, node4, 4.0, HIGHWAY, 2.0),
            DirectedRoad(node5, node6, 10.0, HIGHWAY, 3.0),
            DirectedRoad(node6, node5, 10.0, HIGHWAY, 3.0),
            DirectedRoad(node6, node8, 8.0, LOCAL, 4.0),
            DirectedRoad(node8, node6, 8.0, LOCAL, 4.0),
            DirectedRoad(node6, node7, 7.0, COLLECTOR, 2.0),
            DirectedRoad(node7, node6, 7.0, COLLECTOR, 2.0),
            DirectedRoad(node7, node8, 2.0, HIGHWAY, 5.0),
            DirectedRoad(node8, node7, 2.0, HIGHWAY, 5.0),
            DirectedRoad(node8, node9, 10.0, COLLECTOR, 2.0),
            DirectedRoad(node9, node8, 10.0, COLLECTOR, 2.0),
            DirectedRoad(node7, node9, 1.0, TOLL, 1.0),
            DirectedRoad(node9, node7, 1.0, TOLL, 1.0),
            }

        for road in expected_roads:
            self.assertTrue(str(road) in str(self.road_map), f"road {str(road)} is missing from road map")

        expected_roads_str = ""
        for road in expected_roads:
            expected_roads_str += str(road) + "\n"
        for road in all_roads:
            self.assertTrue(str(road) in expected_roads_str, f"road {str(road)} is in road map, but shouldn't be")


    def _print_path_description(self, start, end, restricted_roads):
        constraint = ""
        if restricted_roads != []:
            constraint += " and without using the {} line(s)".format(
                restricted_roads)
        #print("------------------------")
        #print("Shortest path from Node {} to {} {}".format(
        #    start, end, constraint))

    def _test_path(self, graph, expected_path, expected_time, message="", restricted_roads=[]):
        start, end = expected_path[0], expected_path[-1]
        self._print_path_description(start, end, restricted_roads)
        student_path = find_shortest_path(graph, start, end, restricted_roads)
        self.assertNotEqual(student_path, None, "Your solution returned None, but there is a possible path.")
        self.assertEqual(student_path[0], expected_path, message)
        self.assertEqual(student_path[1], expected_time,
                         "Time incorrect: " + message)

    def _test_impossible_path(self, graph,
                              start,
                              end,
                              restricted_roads=[], message=""):

        self._print_path_description(start, end, restricted_roads)
        student_path = find_shortest_path(graph, start, end, restricted_roads)
        self.assertEqual(student_path, None, message)

    def test_3_small_map_one_step(self):
        expected_path = [self.n0, self.n1]
        expected_time = 10
        self._test_path(self.small_map, expected_path=expected_path, expected_time=expected_time,
                        message="The path goes one step. Make sure you are looking at all of the neighboring nodes.")

    def test_3_small_map_three_step(self):
        expected_path = [self.n0, self.n3, self.n4, self.n2]
        expected_time = 15
        self._test_path(self.small_map, expected_path=expected_path, expected_time=expected_time,
                        message="The best path uses three edges. Make sure your algorithm updates for better paths.")

    def test_3_map1_path_one_step(self):
        expected_path = [self.n0, self.n1]
        expected_time = 15
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time,
                        message="The path goes one step. Make sure you are looking at all of the neighboring nodes.")

    def test_3_map2_path_limited_time(self):
        expected_path = [self.n0, self.n2, self.n4, self.n5]
        expected_time = 12.75
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time,
                        message="Make sure your algorithm is finding the shortest path.")

    def test_3_map3_path_restricted_path(self):
        expected_path = [self.n0, self.n2, self.n3]
        expected_time = 11.5
        restricted_roads = ['highway']
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time, restricted_roads=restricted_roads,
                        message="The path tests having a restricted list of road types. Make sure your algorithm is finding the shortest correct path.")

    def test_3_map_path_start_end_same(self):
        student_path = find_shortest_path(self.road_map, self.n1, self.n1, [])
        self.assertEqual(
            student_path[0], [self.n1], "If the start and end are the same, the path should be the start node")
        self.assertEqual(
            student_path[1], 0, "If the start and end are the same, the time traveled should be zero")

    def test_3_map_path_same_length_different_time(self):
        expected_path = [self.n0, self.n2, self.n3, self.n6]
        expected_time = 16.5
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time,
                        message="Should find path that has the shortest length of all edges combined")

    def test_3_path_multiple_roads_not_allowed(self):
        expected_path = [self.n0, self.n1, self.n3, self.n8, self.n7, self.n9]
        expected_time = 39
        restricted_roads = ['hill', 'local']
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time, restricted_roads=restricted_roads,
                        message="Make sure your search works with multiple restricted roads")

    def test_3_impossible_path_no_highway(self):
        start = self.n0
        end = self.n10
        restricted_roads = ['highway']
        self._test_impossible_path(self.road_map, start=start, end=end, restricted_roads=restricted_roads,
                                   message="Should be impossible")

    def test_3_impossible_path_no_highway_no_local(self):
        start = self.n1
        end = self.n9
        restricted_roads = ['highway', 'local']
        self._test_impossible_path(self.road_map, start=start, end=end, restricted_roads=restricted_roads,
                                   message="Should be impossible")

    def test_3_map_traverse_hill(self):
        expected_path = [self.n0, self.n2, self.n3]
        expected_time = 11.5
        self._test_path(self.road_map, expected_path=expected_path, expected_time=expected_time,
                        message="The path has two edges. Make sure you are looking at all of the neighboring nodes.")

    def test_4a_find_shortest_path_no_traffic(self):
        start, end = Node('N0'), Node('N9')
        expected_path = [Node('N0'), Node('N2'), Node('N3'), Node('N6'), Node('N7'), Node('N9')]
        student_path = find_shortest_path_no_traffic(ROADMAP_FILENAME, start, end)
        self.assertEqual(list, type(student_path), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, student_path, "Make sure your find_shortest_path_no_traffic is correct")

    def test_4b_find_shortest_path_restricted_avoid_local(self):
        start, end = Node('N3'), Node('N6')
        expected_path = [Node('N3'), Node('N8'), Node('N7'), Node('N6')]
        student_path = find_shortest_path_restricted(ROADMAP_FILENAME, start, end)
        self.assertEqual(list, type(student_path), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, student_path, "Make sure your find_shortest_path_restricted is correct")

    def test_4b_find_shortest_path_restricted_avoid_hill(self):
        start, end = Node('N0'), Node('N3')
        expected_path = [Node('N0'), Node('N1'), Node('N3')]
        student_path = find_shortest_path_restricted(ROADMAP_FILENAME, start, end)
        self.assertEqual(list, type(student_path), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, student_path, "Make sure your find_shortest_path_restricted is correct")

    def test_4b_find_shortest_path_restricted_avoid_both_local_hill(self):
        start, end = Node('N4'), Node('N0')
        expected_path = [Node('N4'), Node('N5'), Node('N6'), Node('N7'), Node('N8'), Node('N3'), Node('N1'), Node('N0')]
        student_path = find_shortest_path_restricted(ROADMAP_FILENAME, start, end)
        self.assertEqual(list, type(student_path), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, student_path, "Make sure your find_shortest_path_restricted is correct")

    def test_4c_find_shortest_path_in_traffic_no_toll(self):
        start, end = Node('N0'), Node('N9')
        expected_path = [Node('N0'), Node('N2'), Node('N3'), Node('N8'), Node('N9')]
        student_path = find_shortest_path_in_traffic_no_toll(ROADMAP_FILENAME, start, end)
        self.assertEqual(list, type(student_path), "Make sure you are returning the correct type")
        self.assertEqual(expected_path, student_path, "Make sure your find_shortest_path_in_traffic is correct")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(InternalPs2Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
