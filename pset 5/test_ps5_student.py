import unittest
import numpy as np
import math
import warnings

import ps5

class TestPS5(unittest.TestCase):

    def test_01_linear_regression(self):
        #simple y = x case
        x = np.array([1,2,3,4,5,6,7,8,9,10])
        y = np.array([1,2,3,4,5,6,7,8,9,10])
        (m, b) = ps5.linear_regression(x, y)
        self.assertEqual(m, 1, "Calculated slope is incorrect")
        self.assertEqual(b, 0, "Calculated intercept is incorrect")

        #y = 5x - 3 case
        x = np.array([-5, -3, -1, 1, 2, 6, 10])
        y = np.array([-28, -18, -8, 2, 7, 27, 47])
        (m, b) = ps5.linear_regression(x, y)
        self.assertEqual(m, 5, "Calculated slope is incorrect")
        self.assertEqual(b, -3, "Calculated intercept is incorrect")

        #not exact line case - also tests for float handling
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
        y = np.array([-10,2,1,5,12,13,15,14,19,25,30,29])
        (m, b) = ps5.linear_regression(x, y)
        self.assertTrue(math.isclose(3.241, m, rel_tol=1e-3), "Calculated slope is incorrect")
        self.assertTrue(math.isclose(-4.910, b, rel_tol=1e-3), "Calculated intercept is incorrect")


    def test_02_squared_error(self):
        #easy case
        x = np.array([1,2,3,4,5,6,7,8,9,10])
        y = np.array([1,2,3,4,5,6,7,8,9,10])
        m = 1
        b = 0
        sqe = ps5.squared_error(x, y, m ,b)
        self.assertEqual(sqe, 0, "Squared Error incorrect")

        #interesting case
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
        y = np.array([-10,2,1,5,12,13,15,14,19,25,30,29])
        m = 3
        b = -5
        sqe = ps5.squared_error(x, y, m ,b)
        self.assertEqual(sqe, 119, "Squared Error incorrect")


    def test_03_generate_polynomial_models(self):
        degs_msg = "make_models should return one model for each given degree"
        list_type_msg = "make_models should return a list of models"
        array_type_msg = "each model returned by make_models should be of type np.array"
        coefficient_mismatch = "coefficients of returned model are not as expected"

        # simple y = x case.
        x = np.array(range(50))
        y = np.array(range(50))
        degrees = [1]
        models = ps5.generate_polynomial_models(x, y, degrees)

        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        self.assertIsInstance(models[0], np.ndarray, array_type_msg)
        self.assertTrue(np.allclose(models[0], np.polyfit(x, y, 1)), coefficient_mismatch)
        
        # two models for y = 2x case
        y = np.array(range(0,100,2))
        degrees = [1, 2]
        models = ps5.generate_polynomial_models(x, y, degrees)
        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        for m in models:
            self.assertIsInstance(m, np.ndarray, array_type_msg)
        for i in range(2):
            self.assertTrue(np.allclose(models[i], np.polyfit(x,y, degrees[i])), coefficient_mismatch)

        # three models
        degrees = [1,2,20]
        models = ps5.generate_polynomial_models(x, y, degrees)
        self.assertEqual(len(models), len(degrees), degs_msg)
        self.assertIsInstance(models, list, list_type_msg)
        for m in models:
            self.assertIsInstance(m, np.ndarray, array_type_msg)
        for i in range(3):
            self.assertTrue(np.allclose(models[i], np.polyfit(x,y, degrees[i])), coefficient_mismatch)


    def test_04_calculate_annual_temp_averages(self):
        # test for just one city
        climate = ps5.Dataset('data.csv')
        test_years = np.array(range(2008, 2017))
        result = climate.calculate_annual_temp_averages(['SEATTLE'], test_years)
        correct = [10.798633879781422, 11.218767123287673, 11.514383561643836, 10.586849315068493,
                    11.283196721311475, 12.106438356164384, 12.82917808219178, 13.13178082191781, 12.500546448087432]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))
        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index], abs_tol=1e-3)
            self.assertTrue(good_enough, "City averages do not match expected results.\nExpected Results:" + str(correct) + "\nYour Results:" + str(result))

        # national avg check (all cities)
        result = climate.calculate_annual_temp_averages(ps5.CITIES, test_years)
        correct = [16.130025884383087, 16.116286950252345, 16.334981975486663, 16.46957462148522,
                    17.173878343399483, 16.25620043258832, 16.47222062004326, 17.17817591925018, 17.198259994247916]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index], abs_tol=1e-3)
            self.assertTrue(good_enough, "City averages do not match expected results.\nExpected Results:" + str(correct) + "\nYour Results:" + str(result))

        # two-city check
        result = climate.calculate_annual_temp_averages(['TAMPA', 'DALLAS'], test_years)
        correct = [21.76502732240437, 21.245616438356162, 20.80404109589041, 22.039109589041097,
                    22.272062841530055, 21.3113698630137, 20.88123287671233, 22.077945205479455, 22.181557377049177]
        self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

        for index in range(len(correct)):
            good_enough = math.isclose(correct[index], result[index], abs_tol=1e-3)
            self.assertTrue(good_enough, "City averages do not match expected results.\nExpected Results:" + str(correct) + "\nYour Results:" + str(result))


    def test_05_evaluate_models(self):
        x = np.array(range(50))
        y = np.array(range(0,100,2))
        degrees = [1, 2]
        models = ps5.generate_polynomial_models(x, y, degrees)
        r2 = ps5.evaluate_models(x, y, models, False)
        correct_r2 = [1,1]
        self.assertEqual(len(r2), len(correct_r2), "Returned incorrect r^2 values")
        for index in range(len(correct_r2)):
            good_enough = math.isclose(correct_r2[index], r2[index], abs_tol=1e-3)
            self.assertTrue(good_enough, "Returned incorrect r^2 values")


    def test_06_get_max_trend(self):
        # Test 1: Existing positive and negative slope intervals on city data
        temp = ps5.Dataset('data.csv')
        test_years = np.array(range(1961, 2016))
        yearly_temps = temp.calculate_annual_temp_averages(['PORTLAND'], test_years)

        result_neg = ps5.get_max_trend(test_years, yearly_temps, 20, False)
        correct_start = 31
        correct_end = 51
        correct_slope = -0.032388717977292064
        self.assertIsNotNone(result_neg, "Returned None, but valid interval exists.")
        self.assertEqual(correct_start, result_neg[0], "Start year incorrect")
        self.assertEqual(correct_end, result_neg[1], "End year incorrect")
        self.assertTrue(abs(correct_slope-result_neg[2]) <= 1e-8, "Incorrect slope")

        result_pos = ps5.get_max_trend(test_years, yearly_temps, 20, True)
        correct_start = 15
        correct_end = 35
        correct_slope = 0.05643539541645478
        self.assertIsNotNone(result_pos, "Returned None, but valid interval exists.")
        self.assertEqual(correct_start, result_pos[0], "Start year incorrect")
        self.assertEqual(correct_end, result_pos[1], "End year incorrect")
        self.assertTrue(abs(correct_slope-result_pos[2]) <= 1e-8, "Incorrect slope")

        # Test 2: y = 2x
        x = np.array(range(50))
        y = np.array(range(0,100,2))
        result_pos = ps5.get_max_trend(x, y, len(x)//2, True)
        result_neg = ps5.get_max_trend(x, y, len(x)//2, False)
        pos_correct_start = 0
        pos_correct_end = len(x)//2
        pos_correct_slope = 2

        self.assertIsNone(result_neg, "Returned an interval, but should be None.")

        self.assertIsNotNone(result_pos, "Returned None, but valid interval exists.")
        self.assertEqual(pos_correct_start, result_pos[0], "Start year incorrect")
        self.assertEqual(pos_correct_end, result_pos[1], "End year incorrect")
        self.assertTrue(abs(pos_correct_slope-result_pos[2]) <= 1e-8, "Incorrect slope")

        # # Test 3: y = -2x
        x = np.array(range(50))
        y = np.array(range(100,0,-2))
        result_pos = ps5.get_max_trend(x, y, len(x)//2, True)
        result_neg = ps5.get_max_trend(x, y, len(x)//2, False)
        neg_correct_start = 0
        neg_correct_end = len(x)//2
        neg_correct_slope = -2

        self.assertIsNone(result_pos, "Returned an interval, but should be None.")

        self.assertIsNotNone(result_neg, "Returned None, but valid interval exists.")
        self.assertEqual(neg_correct_start, result_neg[0], "Start year incorrect")
        self.assertEqual(neg_correct_end, result_neg[1], "End year incorrect")
        self.assertTrue(abs(neg_correct_slope-result_neg[2]) <= 1e-8, "Incorrect slope")


        # Test 4: y = (x-10)^2
        x = np.array(range(21))
        y = (x-10)**2
        result_pos = ps5.get_max_trend(x, y, 5, True)
        result_neg = ps5.get_max_trend(x, y, 5, False)

        pos_correct_start = 16
        pos_correct_end = 21
        pos_correct_slope = 16.0

        neg_correct_start = 0
        neg_correct_end = 5
        neg_correct_slope = -16.0

        self.assertEqual(pos_correct_start, result_pos[0], "Start year incorrect")
        self.assertEqual(pos_correct_end, result_pos[1], "End year incorrect")
        self.assertTrue(abs(pos_correct_slope-result_pos[2]) <= 1e-8, "Incorrect slope")

        self.assertEqual(neg_correct_start, result_neg[0], "Start year incorrect")
        self.assertEqual(neg_correct_end, result_neg[1], "End year incorrect")
        self.assertTrue(abs(neg_correct_slope-result_neg[2]) <= 1e-8, "Incorrect slope")



    def test_07_get_all_max_trends(self):
        temp = ps5.Dataset('data.csv')
        test_years = np.array(range(1961, 1971))
        yearly_temps = temp.calculate_annual_temp_averages(['PORTLAND'], test_years)

        result = ps5.get_all_max_trends(test_years, yearly_temps)
        correct = [(3, 5, 2.0206939142151246), (3, 6, 0.9937031214911256), (3, 7, 0.6971533797439919), 
                   (2, 7, 0.44123377498315597), (2, 8, 0.25528513682589676), (2, 9, 0.16264380353533894), 
                   (2, 10, 0.145466766652766), (1, 10, 0.09771779324799829), (0, 10, 0.040402949322555)]
        self.assertIsNotNone(result, "Returned None, but valid interval exists.")
        self.assertEqual(len(result),len(test_years) - 1, "Returned list has incorrect number of elements")
        for index in range(len(correct)):
            self.assertTrue(len(result[index]) == 3, "One or more returned tuples have incorrect number of elements.")
            self.assertEqual(correct[index][:-1], result[index][:-1], "Extreme trend range does not match expected results")
            self.assertTrue(abs(correct[index][-1] - result[index][-1]) <= 1e-8, "Extreme trends do not match expected results")
            
        # Test 2: y = x
        x = np.array(range(6))
        y = np.array(range(0,6))
        correct = [(0, 2, 1.0), (0, 3, 1.0), (0, 4, 1.0), (0, 5, 1.0), (0,6,1.0)]
        result = ps5.get_all_max_trends(x, y)
        self.assertIsNotNone(result, "Returned None, but valid interval exists.")
        self.assertEqual(len(result),len(x) - 1, "Returned list has incorrect number of elements")
        for index in range(len(correct)):
            self.assertTrue(len(result[index]) == 3, "One or more returned tuples have incorrect number of elements.")
            self.assertEqual(correct[index][:-1], result[index][:-1], "Extreme trend range does not match expected results")
            self.assertTrue(abs(correct[index][-1] - result[index][-1]) <= 1e-8, "Extreme trends do not match expected results")


        # Test 3: y = -2x
        x = np.array(range(8))
        y = np.array(range(16,0,-2))
        correct = [(0, 2, -2.0), (0, 3, -2.0), (0, 4, -2.0), (0, 5, -2.0), (0, 6, -2.0), (0, 7, -2.0), (0,8,-2.0)]
        result = ps5.get_all_max_trends(x, y)
        self.assertIsNotNone(result, "Returned None, but valid interval exists.")
        self.assertEqual(len(result),len(x) - 1, "Returned list has incorrect number of elements")
        for index in range(len(correct)):
            self.assertTrue(len(result[index]) == 3, "One or more returned tuples have incorrect number of elements.")
            self.assertEqual(correct[index][:-1], result[index][:-1], "Extreme trend range does not match expected results")
            self.assertTrue(abs(correct[index][-1] - result[index][-1]) <= 1e-8, "Extreme trends do not match expected results")

        # Test 4: len(x) < 2
        x = np.array(range(1))
        y = np.array(range(1))
        correct = []
        result = ps5.get_all_max_trends(x,y)
        self.assertEqual(correct, result, "Incorrect result, expected empty list")

        # Test 5: y = (x-10)^2
        x = np.array(range(21))
        y = (x-10)**2

        result = ps5.get_all_max_trends(x,y)

        correct = [(0, 2, -19.0), (0, 3, -18.0), (0, 4, -17.0), (0, 5, -16.0), (0, 6, -15.0),
         (0, 7, -14.0), (0, 8, -13.0), (0, 9, -12.0), (0, 10, -11.0), (0, 11, -10.0), 
         (0, 12, -9.000000000000002), (0, 13, -8.0), (0, 14, -7.0), (0, 15, -6.0), 
         (0, 16, -5.0), (0, 17, -4.0), (0, 18, -2.9999999999999996), (0, 19, -2.0),
         (0, 20, -1.0), (0, 21, None)]

        self.assertIsNotNone(result, "Returned None, but valid interval exists.")
        self.assertEqual(len(result),len(x) - 1, "Returned list has incorrect number of elements")
        for index in range(len(correct)-1):
            self.assertTrue(len(result[index]) == 3, "One or more returned tuples have incorrect number of elements.")
            self.assertEqual(correct[index][:-1], result[index][:-1], "Extreme trend range does not match expected results")
            self.assertTrue(abs(correct[index][-1] - result[index][-1]) <= 1e-8, "Extreme trends do not match expected results")

        self.assertEqual(correct[-1][:-1], result[-1][:-1], "Extreme trend range does not match expected results")
        self.assertIsNone(correct[-1][-1], "Extreme trends do not match expected results, None expected for final value")


    def test_08_calculate_rmse(self):
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        result = ps5.calculate_rmse(np.array(y), np.array(estimate))
        correct = 35.8515457593
        self.assertTrue(math.isclose(result, correct, abs_tol=1e-3), "RMSE value incorrect")

        y = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
        result = ps5.calculate_rmse(np.array(y), np.array(estimate))
        correct = 40.513372278
        self.assertTrue(math.isclose(result, correct, abs_tol=1e-3), "RMSE value incorrect")


    def test_09_evaluate_rmse(self):
        x = np.array(range(50))
        y = np.array(range(0,100,2))
        degrees = [1, 2]
        models = ps5.generate_polynomial_models(x, y, degrees)
        rmse = ps5.evaluate_rmse(x, y, models, False)
        correct_rmse = [0,0]
        self.assertEqual(len(rmse), len(correct_rmse), "RMSE values did not match number of models")
        for index in range(len(correct_rmse)):
            self.assertTrue(math.isclose(correct_rmse[index], rmse[index], abs_tol=1e-8), "Returned incorrect RMSE values")


if __name__ == '__main__':
    # Run the tests and print verbose output to stderr.
    warnings.simplefilter('ignore', np.RankWarning)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS5))
    unittest.TextTestRunner(verbosity=2).run(suite)
