# Test suite for Problem Set 3 (Robot Simulation)
# 6.100B Fall 2022

import sys
import threading
import traceback
import unittest
import random

import ps3

unittest.TestLoader.sortTestMethodsUsing = None

def xyrange(x_upper_bound, y_upper_bound):
    """ Returns the cartesian product of range(x_upper_bound) and range(y_upper_bound).
        Useful for iterating over the tuple coordinates of a room
    """
    for x in range(x_upper_bound):
        for y in range(y_upper_bound):
            yield (x, y) # these are the room tile xy tuples

class ps3_P1A(unittest.TestCase):
    """test the Room base class"""
    def test_room_dust_dusty(self):
        """
        Can fail either because get_dust_amount is working incorrectly
        OR the student is initializing the dust amount incorrectly
        """
        width, height, dust_amount = (3, 4, 1)
        room = ps3.Room(width, height, dust_amount)
        for x, y in xyrange(width, height):
            self.assertEqual(room.get_dust_amount(x, y),dust_amount,
                             "Tile {} was not initialized with correct dust amount".format((x, y))
                             )

    def test_room_dust_clean(self):
        """
        Can fail either because get_dust_amount is working incorrectly
        OR the student is initializing the dust amount incorrectly
        """
        width, height, dust_amount = (3, 4, 0)
        room = ps3.Room(width, height, dust_amount)
        for x, y in xyrange(width, height):
            self.assertEqual(room.get_dust_amount(x, y),dust_amount,
                             "Tile {} was not initialized with correct dust amount".format((x, y))
                             )

    def test_is_tile_cleaned_dusty(self):
        """ Test is_tile_cleaned"""
        width, height, dust_amount = (3, 4, 1)
        room = ps3.Room(width, height, dust_amount)
        # Check all squares are unclean at start, given initial dust > 1
        for x, y in xyrange(width, height):
            self.assertFalse(room.is_tile_cleaned(x, y),
                             "Unclean tile {} was returned as clean".format((x, y))
                             )

    def test_is_tile_cleaned_clean(self):
        """ Test is_tile_cleaned"""
        width, height, dust_amount = (3, 4, 0)
        room = ps3.Room(width, height, dust_amount)
        # Check all squares are unclean at start, given initial dust > 1
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                             "Clean tile {} was returned as unclean".format((x, y))
                             )

    def test_clean_tile_at_position_PosToZero(self):
        """ Test if clean_tile_at_position removes all dust"""
        width, height, dust_amount = (3, 4, 1)
        room = ps3.Room(width, height, dust_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dust_amount)
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                            "Clean tile {} was not marked clean".format((x, y))
                            )

    def test_clean_tile_at_position_PosToPos(self):
        """ Test if clean_tile_at_position removes all dust"""
        width, height, dust_amount = (3, 4, 2)
        room = ps3.Room(width, height, dust_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dust_amount - 1)
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertFalse(room.is_tile_cleaned(x, y),
                            "Unclean tile {} was marked clean".format((x, y))
                            )

    def test_clean_tile_at_position_ZeroToZero(self):
        """ Test if clean_tile_at_position removes all dust"""
        width, height, dust_amount = (3, 4, 0)
        room = ps3.Room(width, height, dust_amount)
        # Clean the tiles and confirm they are marked as clean
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
                # using random.random in case there is any issue with specific parts of a tile
        for x, y in xyrange(width, height):
            self.assertTrue(room.is_tile_cleaned(x, y),
                            "Clean tile {} was marked clean, no negative dust allowed".format((x, y))
                            )

    def test_get_num_cleaned_tiles_FullIn1(self):
        "Test get_num_cleaned_tiles for cleaning subset of room completely with 1 call"
        width, height, dust_amount = (3, 4, 1)
        room = ps3.Room(width, height, dust_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            cleaned_tiles += 1
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                            "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                            )

    def test_get_num_cleaned_tiles_Partial(self):
        "Test get_num_cleaned_tiles for cleaning subset of room incompletely"
        width, height, dust_amount = (3, 4, 2)
        room = ps3.Room(width, height, dust_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                            "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                            )

    def test_get_num_cleaned_tiles_FullIn2(self):
        """Test get_num_cleaned_tiles for cleaning subset of room in two calls"""
        width, height, dust_amount = (3, 4, 2)
        room = ps3.Room(width, height, dust_amount)
        cleaned_tiles = 0
        # Clean some tiles
        for x, y in xyrange(width-1, height-1):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            cleaned_tiles += 1
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, cleaned_tiles,
                             "Number of clean tiles is incorrect: expected {}, got {}".format(cleaned_tiles, num_cleaned)
                             )

    def test_get_num_cleaned_tiles_OverClean(self):
        "Test cleaning already clean tiles does not increment counter"
        width, height, dust_amount = (3, 4, 2)
        room = ps3.Room(width, height, dust_amount)
        # clean all of the tiles in the room
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), dust_amount)
        for x, y in xyrange(width, height):
            room.clean_tile_at_position(ps3.Position(x + random.random(), y + random.random()), 1)
            num_cleaned = room.get_num_cleaned_tiles()
            self.assertEqual(num_cleaned, width * height,
                             "Number of clean tiles is incorrect: re-cleaning cleaned tiles must not increase number of cleaned tiles"
                             )

    def test_is_position_in_room(self):
        "Test is_position_in_room"
        width, height, dust_amount = (3, 4, 2)
        room = ps3.Room(width, height, dust_amount)
        sols = [True, False,True,False,False,False,False,False,False,False,True,False,True,False,False,False,False,False,False,False,False,False,False,False,False]
        count = 0
        for x in [0.0, -0.1, width - 0.1, width, width + 0.1]:
            for y in [0.0, -0.1, height - 0.1, height, height + 0.1]:
                pos = ps3.Position(x, y)
                self.assertEqual(sols[count],room.is_position_in_room(pos),
                                  "position {},{} is incorrect: expected {}, got {}".format(x, y, sols[count], room.is_position_in_room(pos)))
                count += 1

    def test_get_random_position(self): #TODO - DONE
        """Test get_random_position
            checks for distribution of positions and validity of positions
        """
        width, height, dust_amount = (5, 10, 1)
        room = ps3.Room(width, height, dust_amount)
        freq_buckets = {}
        for i in range(50000):
            pos = room.get_random_position()
            # confirm from test that this is a valid position
            self.assertTrue(room.is_position_in_room(pos))
            try:
                x, y = pos.get_x(), pos.get_y()
            except AttributeError:
                self.fail("get_random_position returned {} which is not a Position".format(pos))
            self.assertTrue(0 <= x < width and 0 <= y < height,
                            "get_random_position returned {} which is not in [0, {}), [0, {})".format(pos,width,height))
            x0, y0 = int(x), int(y)
            freq_buckets[(x0, y0)] = freq_buckets.get((x0, y0), 0) + 1
        for t in xyrange(width, height):
            num_in_bucket = freq_buckets.get(t, 0)
            self.assertTrue(
                # This is a 99.7% confidence interval for a uniform
                # distribution. Fail if the total of any bucket falls outside
                # this range.
                865 < num_in_bucket < 1150,
                "The distribution of positions from get_random_position "
                "looks incorrect (it should be uniform)")

    def test_get_num_tiles(self): #TODO - DONE
        """ test get_num_tiles method"""
        widths = [10, 8, 4, 4, 2, 4, 1, 6, 7, 5, 3]
        heights = [6, 8, 9, 3, 5, 6, 2, 1, 3, 1, 7]
        sols = [60, 64, 36,12,10,24,2,6,21,5, 21]
        for i in range(11):
            # width, height, dust_amount = (random.randint(1,10), random.randint(1,10), 1)
            width, height, dust_amount = (widths[i], heights[i], 1)
            room_num_tiles = ps3.Room(width, height, dust_amount).get_num_tiles()
            sol_room_tiles = sols[i]
            self.assertEqual(room_num_tiles, sol_room_tiles,
                             "student code number of room tiles = {}, not equal to solution code num tiles {}".format(room_num_tiles, sol_room_tiles)
                             )

class ps3_P1B(unittest.TestCase):
    """test the Robot abstract base class"""
    def test_unimplemented_methods(self): #TODO - shouldn't need it
        """Test if student implemented methods in Robot abstract class that should not be implemented"""
        room = ps3.Room(2,2,1)
        robot = ps3.Robot(room,1,1)
        self.assertRaises(NotImplementedError, robot.update_position_and_clean)

    def test_getset_direction(self): #TODO - shouldn't need it
        """Test get_direction and set_direction"""
        # instantiate Room from solutions for testing
        width, height, dust_amount = (3, 4, 2)
        solution_room = ps3.Room(width, height, dust_amount)

        robots = [ps3.Robot(solution_room, 1.0, 1) for i in range(5)]
        directions = [1, 333, 105, 75, 74.3]
        for dir_index, robot in enumerate(robots):
            robot.set_direction(directions[dir_index])
        for dir_index, robot in enumerate(robots):
            robot_dir = robot.get_direction()
            self.assertEqual(robot_dir, directions[dir_index],
                              "Robot direction set or retrieved incorrectly: expected {}, got {}".format(directions[dir_index], robot_dir)
                              )


class ps3_P3(unittest.TestCase):
    """This  tests Room and NormalRobot in various ways"""
    def createRoomAndRobots(self, num_robots):
        r = ps3.Room(5, 7, 1)
        robots = [ps3.NormalRobot(r, 1.0, 1) for i in range(num_robots)]
        return r, robots

    def test_BoundaryConditions(self):
        "Test strict inequalities in random positions for the Room and NormalRobot"
        for m in range(7000):
            r, robots = self.createRoomAndRobots(4)
            for r in robots:
                p = r.get_position()
                d = r.get_direction()
                try:
                    x, y = p.get_x(), p.get_y()
                except AttributeError:
                    self.fail("get_position returned %r which is not a Position" % (p,))
                self.assertTrue(x < 5 and y < 7,
                                "Robot position was set to %r, "
                                "which is not in [0, 5), [0, 7)" %
                                ((p.get_x(), p.get_y()),))
                self.assertTrue(0 <= d < 360,
                                "Robot direction was set to %r, "
                                "which is not in [0, 360)" % (d,))

    def testRobot(self):
        "Test NormalRobot"
        pos_buckets = {}
        dir_buckets = {}
        skip_pos_distribution_test = False
        for m in range(7000):
            r, robots = self.createRoomAndRobots(4)
            for r in robots:
                p = r.get_position()
                d = r.get_direction()
                try:
                    x, y = p.get_x(), p.get_y()
                except AttributeError:
                    self.fail("get_position returned %r which is not a Position" % (p,))
                self.assertTrue(0 <= x <= 5 and 0 <= y <= 7,
                                "Robot position was set to %r, "
                                "which is not in [0, 5), [0, 7)" %
                                ((p.get_x(), p.get_y()),))
                self.assertTrue(0 <= d <= 360,
                                "Robot direction was set to %r, "
                                "which is not in [0, 360)" % (d,))
                x0, y0 = int(p.get_x()), int(p.get_y())
                pos_buckets[(x0, y0)] = pos_buckets.get((x0, y0), 0) + 1
                dir_buckets[int(d / 10)] = dir_buckets.get(int(d / 10), 0) + 1
        # Test that positions are correctly distributed
        if not skip_pos_distribution_test:
            for t in xyrange(5, 7):
                num_in_bucket = pos_buckets.get(t, 0)
                self.assertTrue(
                    685 < num_in_bucket < 915,
                    "The distribution of positions on new Robot objects "
                    "looks incorrect (it should be uniform)")

        # Test that directions are correctly distributed
        for t in range(36):
            num_in_bucket = dir_buckets.get(t, 0)
            self.assertTrue(
                658 < num_in_bucket < 898,
                "The distribution of positions from get_random_position "
                "looks incorrect (it should be uniform)")

    def test_update_position_and_cleanNormalRobot(self):
        "Test NormalRobot.update_position_and_clean"
        r = ps3.Room(3, 5, 1)
        robot = ps3.NormalRobot(r, 1.0, 1)
        robot.set_position(ps3.Position(1.5, 2.5))
        robot.set_direction(90)
        robot.update_position_and_clean()
        self.assertEqual(robot.get_direction(), 90,
                          "Robot direction is updated incorrectly by update_position_and_clean: expected %r, got %r" %
                          (90, robot.get_direction()))
        # check if robot position is valid
        robotPos = robot.get_position()
        correctPos = ps3.Position(2.5, 2.5)
        self.assertTrue(robotPos.get_x() == correctPos.get_x() and robotPos.get_y() == correctPos.get_y(),
                          "Robot position is updated incorrectly by update_position_and_clean: expected %r, got %r" %
                          (ps3.Position(2.5, 2.5), robot.get_position()))
        self.assertTrue(2>=r.get_num_cleaned_tiles() >= 1,
                        "update_position_and_clean should have marked one or two tiles as clean")
        self.assertTrue(r.is_tile_cleaned(1, 2) or r.is_tile_cleaned(2, 2),
                        "update_position_and_clean should have marked either (1, 2) or (2, 2) as clean")

        # Simulate a lot of time passing...
        for i in range(20):
            robot.update_position_and_clean()
            self.assertTrue(r.is_position_in_room(robot.get_position()),
                            "Robot position %r is not in room!" % (robot.get_position(),))
        self.assertNotEqual(robot.get_direction(), 90,
                          "Robot direction should have been changed in update_position_and_clean")
        self.assertTrue(r.get_num_cleaned_tiles() >= 1,
                        "update_position_and_clean should have marked another tile as clean")

"""The SIMULATION_TIME_LIMIT, SimulationThread class and SimulationTester class
    are all designed to help test various simulations for problems 4 and 5
"""
SIMULATION_TIME_LIMIT = 40.0

class SimulationThread(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.result = []
        self.exception_info = None
        self.args = args
    def run(self):
        try:
            # run the simulation 5 times for each student
            for i in range(5):
                self.result.append(ps3.run_simulation(*self.args))
        except Exception:
            self.exception_info = sys.exc_info()
    def getResult(self):
        return self.result
    def getExceptionInfo(self):
        return self.exception_info

class SimulationTester(unittest.TestCase):
    def run_simulation(self, bounds, parameters):
        """
        Tests ps3.run_simulation.  The number of time-steps
        ps3.run_simulation takes must fall between any of
        the (LOWER, UPPER) bound tuples inside bounds.

        ps3.run_simulation must also finish within a timelimit
        to be considered passing.  Threads are used to time
        a simulation.

        bounds: tuple of (lower, upper) bounds on the number of
            steps a simulation should take.
        parameters: parameters to be passed into ps3.run_simulation

        """
        thr = SimulationThread(*parameters)
        # Set daemon flag, so we can quit the test even if simulation threads
        # are still running
        thr.setDaemon(True)
        thr.start()
        # Allow SIMULATION_TIME_LIMIT seconds for test to finish
        thr.join(SIMULATION_TIME_LIMIT)
        if thr.is_alive():
            self.fail("Simulation took too long (more than %d seconds)" %
                    SIMULATION_TIME_LIMIT)
        elif thr.getExceptionInfo():
            self.fail("Exception occurred in simulation thread:\n\n%s" %
                    "".join(traceback.format_exception(*thr.getExceptionInfo())))
        else:
            actual_list = thr.getResult()
            actual_str = str(actual_list)
            intervals_str = " or ".join([("[%.1f, %.1f]" % b) for b in bounds])
            # check which responses are in the correct range
            passed = []
            for result in actual_list:
                passed.append(any([LB < result < UB for LB, UB in bounds]))
            # ensure that they they pass atleast 3 out of 5 times. Majority of the runs
            self.assertTrue(
                max(set(passed), key=passed.count),
                "Simulation output was outside of 99.7%% confidence interval over 5 trials !\n"
                "Robots: %d; Speed: %.1f; Cleaning Volume: %d; Dimensions: %dx%d; "
                "dust Amount: %d; Coverage: %.2f; Trials: %d; Robot type: %r\n"
                "Actual output: %r; acceptable intervals: %s"
                % (parameters + (actual_str, intervals_str)))

class ps3_P5_Normal(SimulationTester):
    """test the simulation time cleaning the Room with a NormalRobot"""
    def testNormalSimulation1(self):
        "Test cleaning 100% of a 5x5 room"
        try:
            self.run_simulation(((142, 174),), (1, 1.0, 1, 5, 5, 1, 1.0, 100, ps3.NormalRobot))
        except:
            print ("Unexpected error:", sys.exc_info()[1])
            raise
    def testNormalSimulation2(self):
        "Test cleaning 75% of a 10x10 room (Normal Robot)"
        self.run_simulation(((183, 198),), (1, 1.0, 1, 10, 10, 1, 0.75, 100, ps3.NormalRobot))
    def testNormalSimulation3(self):
        "Test cleaning 90% of a 10x10 room (Normal Robot)"
        self.run_simulation(((298, 327),), (1, 1.0, 1, 10, 10, 1, 0.9, 100, ps3.NormalRobot))
    def testNormalSimulation4(self):
        "Test multiple robots (95% of a 20x20 room with 5 robots (Normal Robot))"
        self.run_simulation(((289, 303),), (5, 1.0, 1, 20, 20, 1, 0.95, 100, ps3.NormalRobot))
    def testNormalSimulation5(self):
        "Test multiple robots and different speeds (90% of a 10x10 room with 3 robots of speed 0.5 (Normal Robot))"
        self.run_simulation(((155, 180),), (3, 0.5, 1, 10, 10, 1, 0.9, 100, ps3.NormalRobot))
    def testNormalSimulation6(self):
        "Test cleaning 100% of a 5x5 room (Normal Robot, 5 dust/tile, cleaning_volume = 3)"
        self.run_simulation(((206, 266),(180, 240)), (1, 1.0, 3, 5, 5, 5, 1.0, 100, ps3.NormalRobot))
    def testNormalSimulation7(self):
        "Test cleaning 100% of a 5x5 room (Normal Robot, 6 dust/tile, cleaning_volume = 3)"
        self.run_simulation(((206, 266),(180, 240)), (1, 1.0, 3, 5, 5, 6, 1.0, 100, ps3.NormalRobot))
    def testNormalSimulation8(self):
        "Test multiple robots (95% of a 10x10 room with 5 robots (Normal Robot)) cleaning_volume = 2, 6 dust/tile"
        self.run_simulation(((137, 198),(130, 190)), (5, 1.0, 2, 10, 10, 6, 0.95, 100, ps3.NormalRobot))
    def testNormalSimulation9(self):
        """Test multiple robots and different speeds (90% of a 5x5 room with 3 robots of speed 0.5
        (Normal Robot)), cleaning_volume = 2, 6 dust/tile"""
        self.run_simulation(((48, 108), (45, 104)), (3, 0.5, 2, 5, 5, 6, 0.9, 100, ps3.NormalRobot))


class ps3_P5_Clumsy(SimulationTester):
    """test the simulation time cleaning the Room with a ClumsyRobot"""
    def testClumsySimulation1(self):
        "Test cleaning 100% of a 5x5 room with ClumsyRobot"
        ps3.ClumsyRobot.set_dust_probability(0.03)
        self.run_simulation(((203, 281),), (1, 1.0, 1, 5, 5, 1, 1.0, 100, ps3.ClumsyRobot))
    def testClumsySimulation2(self):
        "Test cleaning 75% of a 10x10 room with ClumsyRobot"
        ps3.ClumsyRobot.set_dust_probability(0.10)
        self.run_simulation(((252, 287),), (1, 1.0, 1, 10, 10, 1, 0.75, 100, ps3.ClumsyRobot))
    def testClumsySimulation3(self):
        "Test cleaning 100% of a 5x5 room with 2 ClumsyRobots"
        ps3.ClumsyRobot.set_dust_probability(0.12)
        self.run_simulation(((836,1362),),(2, 1.0, 2, 5, 5, 5, 1.0, 100, ps3.ClumsyRobot))
    def testClumsySimulation4(self):
        "Test cleaning 75% of a 10x10 room with 4 ClumsyRobots"
        ps3.ClumsyRobot.set_dust_probability(0.16)
        self.run_simulation(((135,149),),(4, 1.0, 3, 10, 10, 5, 0.75, 100, ps3.ClumsyRobot))

class ps3_P5_Sensing(SimulationTester):
    """test the simulation time cleaning the Room with a SensingRobot"""
    def testSensingSimulation1(self):
        "Test cleaning 100% of a 5x5 room with SensingRobot"
        self.run_simulation(((41, 56),), (1, 1.0, 1, 5, 5, 1, 1.0, 100, ps3.SensingRobot))
    def testSensingSimulation2(self):
        "Test cleaning 75% of a 10x10 room with SensingRobot"
        self.run_simulation(((91, 107),), (1, 1.0, 1, 10, 10, 1, 0.75, 100, ps3.SensingRobot))
    def testSensingSimulation3(self):
        "Test cleaning 90% of a 10x10 room with SensingRobot"
        self.run_simulation(((143, 169),), (1, 1.0, 1, 10, 10, 1, 0.9, 100, ps3.SensingRobot))
    def testSensingSimulation4(self):
        "Test cleaning 100% of a 5x5 room with 2 SensingRobots"
        self.run_simulation(((46, 53),), (2, 1.0, 2, 5, 5, 5, 1.0, 100, ps3.SensingRobot))
    def testSensingSimulation5(self):
        "Test cleaning 75% of a 10x10 room with 3 SensingRobots"
        self.run_simulation(((46, 50),), (4, 1.0, 3, 10, 10, 5, 0.75, 100, ps3.SensingRobot))
    def testSensingSimulation6(self):
        "Test cleaning 90% of a 10x10 room with 3 SensingRobots"
        self.run_simulation(((84, 89),), (5, 1.0, 3, 10, 10, 10, 0.9, 100, ps3.SensingRobot))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # Feel free to comment out test suites for parts you're not
    # actively working on to save time!
    suite.addTest(unittest.makeSuite(ps3_P1A))
    suite.addTest(unittest.makeSuite(ps3_P1B))
    suite.addTest(unittest.makeSuite(ps3_P3))
    suite.addTest(unittest.makeSuite(ps3_P5_Normal))
    SIMULATION_TIME_LIMIT = 100.0  # reset the time limit for the cheap robot
    suite.addTest(unittest.makeSuite(ps3_P5_Clumsy))
    SIMULATION_TIME_LIMIT = 400.0  # reset the time limit for the Sensing robot
    suite.addTest(unittest.makeSuite(ps3_P5_Sensing))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
