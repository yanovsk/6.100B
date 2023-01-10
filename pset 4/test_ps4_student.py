import unittest
import numpy as np
import random
import sys

from ps4 import predicted_sea_level_rise, simulate_year, wait_a_bit, simulate_water_levels, repair_only, prepare_immediately

SEA_LEVEL_DATA = np.array([ [2020.0, 4.15, 3.9, 4.4, 0.12755336423116348], 
                        [2021.0, 4.180000000000001, 3.92, 4.44, 0.13265549880041005], 
                        [2022.0, 4.21, 3.94, 4.48, 0.1377576333696566], 
                        [2023.0, 4.24, 3.96, 4.5200000000000005, 0.14285976793890318], 
                        [2024.0, 4.27, 3.98, 4.5600000000000005, 0.14796190250814975], 
                        [2025.0, 4.3, 4.0, 4.6, 0.1530640370773963], 
                        [2026.0, 4.33, 4.02, 4.64, 0.15816617164664287], 
                        [2027.0, 4.359999999999999, 4.04, 4.68, 0.16326830621588945], 
                        [2028.0, 4.39, 4.06, 4.72, 0.16837044078513602], 
                        [2029.0, 4.419999999999999, 4.08, 4.76, 0.17347257535438257], 
                        [2030.0, 4.449999999999999, 4.1, 4.8, 0.17857470992362914], 
                        [2031.0, 4.484999999999999, 4.119999999999999, 4.85, 0.18622791177749892], 
                        [2032.0, 4.52, 4.14, 4.8999999999999995, 0.1938811136313687], 
                        [2033.0, 4.555, 4.16, 4.95, 0.20153431548523848], 
                        [2034.0, 4.59, 4.18, 5.0, 0.20918751733910826], 
                        [2035.0, 4.625, 4.199999999999999, 5.05, 0.21684071919297804], 
                        [2036.0, 4.659999999999999, 4.22, 5.1, 0.22449392104684784], 
                        [2037.0, 4.694999999999999, 4.24, 5.1499999999999995, 0.23214712290071762], 
                        [2038.0, 4.7299999999999995, 4.26, 5.2, 0.2398003247545874], 
                        [2039.0, 4.765, 4.279999999999999, 5.25, 0.24745352660845718], 
                        [2040.0, 4.8, 4.3, 5.3, 0.25510672846232696], 
                        [2041.0, 4.84, 4.32, 5.359999999999999, 0.26531099760082005], 
                        [2042.0, 4.88, 4.34, 5.42, 0.27551526673931315], 
                        [2043.0, 4.92, 4.359999999999999, 5.48, 0.28571953587780624], 
                        [2044.0, 4.96, 4.38, 5.54, 0.29592380501629933], 
                        [2045.0, 5.0, 4.4, 5.6, 0.3061280741547924], 
                        [2046.0, 5.04, 4.42, 5.66, 0.3163323432932855], 
                        [2047.0, 5.08, 4.4399999999999995, 5.720000000000001, 0.32653661243177856], 
                        [2048.0, 5.12, 4.46, 5.78, 0.33674088157027166], 
                        [2049.0, 5.16, 4.48, 5.84, 0.34694515070876475], 
                        [2050.0, 5.2, 4.5, 5.9, 0.35714941984725784], 
                        [2051.0, 5.245, 4.52, 5.970000000000001, 0.36990475627037417], 
                        [2052.0, 5.29, 4.54, 6.04, 0.38266009269349044], 
                        [2053.0, 5.335, 4.5600000000000005, 6.11, 0.39541542911660676], 
                        [2054.0, 5.38, 4.58, 6.18, 0.40817076553972303], 
                        [2055.0, 5.425000000000001, 4.6, 6.25, 0.42092610196283936], 
                        [2056.0, 5.470000000000001, 4.62, 6.32, 0.43368143838595563], 
                        [2057.0, 5.515000000000001, 4.640000000000001, 6.39, 0.44643677480907196], 
                        [2058.0, 5.5600000000000005, 4.66, 6.46, 0.4591921112321883], 
                        [2059.0, 5.605, 4.68, 6.529999999999999, 0.47194744765530455], 
                        [2060.0, 5.65, 4.7, 6.6, 0.4847027840784209], 
                        [2061.0, 5.695, 4.720000000000001, 6.67, 0.49745812050153726], 
                        [2062.0, 5.74, 4.74, 6.739999999999999, 0.5102134569246537], 
                        [2063.0, 5.785, 4.76, 6.81, 0.52296879334777], 
                        [2064.0, 5.83, 4.78, 6.88, 0.5357241297708865], 
                        [2065.0, 5.875, 4.800000000000001, 6.949999999999999, 0.5484794661940029], 
                        [2066.0, 5.92, 4.82, 7.02, 0.5612348026171192], 
                        [2067.0, 5.965, 4.84, 7.09, 0.5739901390402357], 
                        [2068.0, 6.01, 4.86, 7.16, 0.5867454754633521], 
                        [2069.0, 6.055, 4.880000000000001, 7.2299999999999995, 0.5995008118864684], 
                        [2070.0, 6.1, 4.9, 7.3, 0.6122561483095849], 
                        [2071.0, 6.145, 4.91, 7.38, 0.6301136193019478], 
                        [2072.0, 6.1899999999999995, 4.92, 7.46, 0.6479710902943105], 
                        [2073.0, 6.234999999999999, 4.930000000000001, 7.54, 0.6658285612866734], 
                        [2074.0, 6.279999999999999, 4.94, 7.62, 0.6836860322790363], 
                        [2075.0, 6.324999999999999, 4.95, 7.699999999999999, 0.7015435032713992], 
                        [2076.0, 6.37, 4.96, 7.779999999999999, 0.719400974263762], 
                        [2077.0, 6.415, 4.97, 7.859999999999999, 0.7372584452561249], 
                        [2078.0, 6.46, 4.98, 7.9399999999999995, 0.7551159162484877], 
                        [2079.0, 6.505, 4.99, 8.02, 0.7729733872408506], 
                        [2080.0, 6.55, 5.0, 8.1, 0.7908308582332135], 
                        [2081.0, 6.6049999999999995, 5.02, 8.19, 0.8086883292255764], 
                        [2082.0, 6.66, 5.04, 8.28, 0.8265458002179393], 
                        [2083.0, 6.715, 5.0600000000000005, 8.37, 0.8444032712103022], 
                        [2084.0, 6.77, 5.08, 8.459999999999999, 0.8622607422026651], 
                        [2085.0, 6.824999999999999, 5.1, 8.55, 0.880118213195028], 
                        [2086.0, 6.88, 5.12, 8.64, 0.8979756841873909], 
                        [2087.0, 6.935, 5.140000000000001, 8.73, 0.9158331551797539], 
                        [2088.0, 6.989999999999999, 5.16, 8.82, 0.9336906261721168], 
                        [2089.0, 7.045, 5.18, 8.91, 0.9515480971644797], 
                        [2090.0, 7.1, 5.2, 9.0, 0.9694055681568426], 
                        [2091.0, 7.16, 5.220000000000001, 9.1, 0.9898141064338288], 
                        [2092.0, 7.22, 5.24, 9.2, 1.010222644710815], 
                        [2093.0, 7.279999999999999, 5.26, 9.3, 1.030631182987801], 
                        [2094.0, 7.34, 5.28, 9.4, 1.0510397212647873], 
                        [2095.0, 7.4, 5.300000000000001, 9.5, 1.0714482595417734], 
                        [2096.0, 7.46, 5.32, 9.6, 1.0918567978187594], 
                        [2097.0, 7.52, 5.34, 9.7, 1.1122653360957455], 
                        [2098.0, 7.58, 5.36, 9.8, 1.1326738743727316], 
                        [2099.0, 7.640000000000001, 5.380000000000001, 9.9, 1.153082412649718], 
                        [2100.0, 7.7, 5.4, 10.0, 1.173490950926704]])

class TestPS4(unittest.TestCase):
    def test_part_1_1_predicted_sea_level_rise(self):
        student_out = predicted_sea_level_rise()
        expected_out = SEA_LEVEL_DATA.copy()

        # determining equality between floats
        epsilon = 1e-7

        self.assertIsNotNone(student_out, "predicted_sea_level_rise() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f"predicted_sea_level_rise() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertEqual(expected_out.shape[0], student_out.shape[0], f"predicted_sea_level_rise() returned incorrect number of rows. Expected: {len(expected_out)} Got: {student_out.shape[0]}")
        self.assertEqual(expected_out.shape[1], student_out.shape[1], f"predicted_sea_level_rise() returned incorrect number of columns. Expected: {len(expected_out[0])} Got: {student_out.shape[1]}")
        for row in expected_out:
            year = row[0]
            student_row = None
            for r in student_out:
                if r[0] == year:
                    student_row = r
                    break
            self.assertIsNotNone(student_row, f"predicted_sea_level_rise() is missing data for year {year}")
            self.assertAlmostEqual(row[1], student_row[1], delta=epsilon, msg=f"For year {year}, expected mean of {row[1]} but got mean of {student_row[1]}")
            self.assertAlmostEqual(row[2], student_row[2], delta=epsilon, msg=f"For year {year}, expected lower 25% of {row[2]} but got lower 25% of {student_row[2]}")
            self.assertAlmostEqual(row[3], student_row[3], delta=epsilon, msg=f"For year {year}, expected upper 25% of {row[3]} but got upper 25% of {student_row[3]}")
            self.assertAlmostEqual(row[4], student_row[4], delta=epsilon, msg=f"For year {year}, expected std_dev of {row[4]} but got std_dev of {student_row[4]}")

            
    def test_part_1_2_simulate_year_1(self):
        #tests simulate_year for N=1

        NUM_TRIALS = 10000
        YEAR = 2073
        N = 1

        epsilon = 1e-1
        
        student_out = simulate_year(SEA_LEVEL_DATA, YEAR, N)

        self.assertIsNotNone(student_out, "simulate_year() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f"simulate_year() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertTrue(len(student_out.shape)==1, f"Expected simulate_year() to return a 1 dimensional numpy array. Got numpy array of shape {student_out.shape}")
        self.assertEqual(N, student_out.shape[0], f"Expected simulate_year() to return 1-D numpy array with {N} elements. Got {student_out.shape[0]}")

        student_outputs = []
        for i in range(NUM_TRIALS):
            student_outputs.append(simulate_year(SEA_LEVEL_DATA, YEAR, N))
        
        student_mean = np.mean(np.array(student_outputs))
        student_std = np.std(np.array(student_outputs))

        expected_mean = SEA_LEVEL_DATA[YEAR-2020][1]
        expected_std = SEA_LEVEL_DATA[YEAR-2020][4]

        self.assertAlmostEqual(expected_mean, student_mean, delta=epsilon, msg=f"For year {YEAR}, expected simulate_year() to return outputs with mean {expected_mean}. Got {student_mean}")
        self.assertAlmostEqual(expected_std, student_std, delta=epsilon, msg=f"For year {YEAR}, expected simulate_year() to return outputs with std_dev {expected_std}. Got {student_std}")
        
    def test_part_1_2_simulate_year_2(self):
        #tests simulate_year for N>1
        YEAR = 2048
        N = 3

        student_out = simulate_year(SEA_LEVEL_DATA, YEAR, N)

        self.assertIsNotNone(student_out, "simulate_year() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f"simulate_year() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertTrue(len(student_out.shape)==1, f"Expected simulate_year() to return a 1 dimensional numpy array. Got numpy array of shape {student_out.shape}")
        self.assertEqual(N, student_out.shape[0], f"Expected simulate_year() to return 1-D numpy array with {N} elements. Got {student_out.shape[0]}")

        N = 100

        student_out = simulate_year(SEA_LEVEL_DATA, YEAR, N)

        self.assertIsNotNone(student_out, "simulate_year() returned None instead of numpy array!")
        self.assertTrue(type(student_out)==np.ndarray, f"simulate_year() returned incorrect type. Expected numpy array. Got {type(student_out)}")
        self.assertTrue(len(student_out.shape)==1, f"Expected simulate_year() to return a 1 dimensional numpy array. Got numpy array of shape {student_out.shape}")
        self.assertEqual(N, student_out.shape[0], f"Expected simulate_year() to return 1-D numpy array with {N} elements. Got {student_out.shape[0]}")

    def test_part_2_1_simulate_water_levels(self):
        np.random.seed(0)
        random.seed(0)
        expected_output = [4.38, 4.23, 4.34, 4.56, 4.55, 4.15, 4.48, 4.34, 4.37, 4.49, 4.48, 4.76, 4.67, 4.58, 4.68, 4.7, 5.0, 4.65, 4.81, 4.55, 4.15, 5.01, 5.12, 4.71, 5.63, 4.55, 5.05, 5.02, 5.64, 5.67, 5.26, 5.38, 4.95, 4.55, 5.24, 5.49, 6.0, 6.05, 5.38, 5.46, 5.14, 4.99, 4.87, 6.81, 5.56, 5.63, 5.22, 6.41, 5.06, 5.93, 5.55, 6.39, 5.86, 5.45, 6.26, 6.63, 6.42, 6.64, 5.98, 6.22, 6.02, 6.31, 5.99, 5.26, 6.92, 6.47, 5.42, 7.36, 6.14, 7.09, 7.81, 7.29, 8.37, 6.01, 7.76, 6.67, 6.51, 6.88, 7.23, 7.7, 6.33]
        student_output = simulate_water_levels(SEA_LEVEL_DATA)
        
        self.assertIsNotNone(student_output, "simulate_water_levels() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected simulate_water_levels() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected simulate_water_levels() to return list of length {len(expected_output)}. Got {len(student_output)}")
        
        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For simulate_water_levels(), for year {2020+i}, expected water level of {expected_output[i]}. Got {student_output[i]}")

    def test_part_2_2a_repair_only(self):
        np.random.seed(0)
        random.seed(0)

        water_level_loss_no_prevention = np.array([[5,6,7,8,9,10],[0,10,25,45,75,100]]).T

        water_level = [4.4181169189, 4.2432523603, 4.3706582199, 4.6214625724, 4.5992644453, 4.1217571709, 4.5090599508, 4.3305540324, 4.36929164, 4.5048728959, 4.4806502956, 4.8077094626, 4.6958176721, 4.5842193972, 4.7006383708, 4.7112153245, 5.0596676552, 4.6382490475, 4.8194558746, 4.5131621302, 4.0239461998, 5.0466333831, 5.1637915421, 4.667325595, 5.7603494416, 4.4694850712, 5.057247906, 5.0071681917, 5.7350299728, 5.7674485578, 5.2659409422, 5.4116822033, 4.8851984421, 4.4017149723, 5.2107875455, 5.5034190747, 6.1057690809, 6.1546206632, 5.3480698137, 5.4349970042, 5.0443988082, 4.8532731338, 4.7026613805, 7.0006369098, 5.5046611479, 5.5886949656, 5.0821899521, 6.4967656453, 4.8816427442, 5.9030291345, 5.4467139836, 6.4354967208, 5.7956047091, 5.29830571, 6.2570410051, 6.6830600196, 6.4270198357, 6.6807208429, 5.8892521333, 6.1708955803, 5.9163182687, 6.2585304104, 5.8591403032, 4.9780687254, 6.9522959657, 6.4036420727, 5.1356812086, 7.4400261829, 5.9805752222, 7.1038977412, 7.9421856179, 7.3121271211, 8.5915587323, 5.7635439967, 7.84388908, 6.525696556, 6.3270688572, 6.7528239738, 7.1595087113, 7.717170194, 6.070770146]

        expected_output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.3867062080000068, 0.0, 0.0, 0.0, 0.0, 1.8653353239999857, 6.55166168400001, 0.0, 30.41397766399999, 0.0, 2.2899162399999895, 0.2867276679999975, 29.40119891199998, 30.69794231199999, 10.637637688000012, 16.467288131999993, 0.0, 0.0, 8.431501819999987, 20.136762988, 46.346144854, 49.27723979200002, 13.92279254799998, 17.399880168000017, 1.775952328000017, 0.0, 0.0, 100.05095278399997, 20.18644591600001, 23.54779862400001, 3.2875980840000096, 69.805938718, 0.0, 36.12116537999999, 17.868559343999983, 66.12980324799999, 31.824188364, 11.932228400000007, 55.42246030599998, 80.98360117600001, 65.62119014200002, 80.84325057399998, 35.57008533200001, 50.253734818, 36.65273074800002, 55.511824623999985, 34.36561212800001, 0.0, 97.13775794200002, 64.21852436200001, 5.427248344000013, 135.20209463199993, 39.22300888799999, 108.311819296, 175.374849432, 124.97016968799997, 250.9870478759999, 30.541759868000007, 167.51112640000002, 71.54179335999999, 59.62413143199997, 85.169438428, 112.760696904, 157.37361552000004, 44.24620876]
        student_output = repair_only(water_level, water_level_loss_no_prevention)

        self.assertIsNotNone(student_output, "repair_only() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected repair_only() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected repair_only() to return list of length {len(expected_output)}. Got {len(student_output)}")
        
        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For repair_only(), for year {2020+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")

    def test_part_2_2b_wait_a_bit(self):
        np.random.seed(0)
        random.seed(0)

        water_level_loss_no_prevention = np.array([[5,6,7,8,9,10],[0,10,25,45,75,100]]).T
        water_level_loss_with_prevention = np.array([[5,6,7,8,9,10],[0,5,15,30,70,100]]).T

        water_level = [4.4181169189, 4.2432523603, 4.3706582199, 4.6214625724, 4.5992644453, 4.1217571709, 4.5090599508, 4.3305540324, 4.36929164, 4.5048728959, 4.4806502956, 4.8077094626, 4.6958176721, 4.5842193972, 4.7006383708, 4.7112153245, 5.0596676552, 4.6382490475, 4.8194558746, 4.5131621302, 4.0239461998, 5.0466333831, 5.1637915421, 4.667325595, 5.7603494416, 4.4694850712, 5.057247906, 5.0071681917, 5.7350299728, 5.7674485578, 5.2659409422, 5.4116822033, 4.8851984421, 4.4017149723, 5.2107875455, 5.5034190747, 6.1057690809, 6.1546206632, 5.3480698137, 5.4349970042, 5.0443988082, 4.8532731338, 4.7026613805, 7.0006369098, 5.5046611479, 5.5886949656, 5.0821899521, 6.4967656453, 4.8816427442, 5.9030291345, 5.4467139836, 6.4354967208, 5.7956047091, 5.29830571, 6.2570410051, 6.6830600196, 6.4270198357, 6.6807208429, 5.8892521333, 6.1708955803, 5.9163182687, 6.2585304104, 5.8591403032, 4.9780687254, 6.9522959657, 6.4036420727, 5.1356812086, 7.4400261829, 5.9805752222, 7.1038977412, 7.9421856179, 7.3121271211, 8.5915587323, 5.7635439967, 7.84388908, 6.525696556, 6.3270688572, 6.7528239738, 7.1595087113, 7.717170194, 6.070770146]

        expected_output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.3867062080000068, 0.0, 0.0, 0.0, 0.0, 1.8653353239999857, 6.55166168400001, 0.0, 30.41397766399999, 0.0, 2.2899162399999895, 0.2867276679999975, 29.40119891199998, 30.69794231199999, 10.637637688000012, 16.467288131999993, 0.0, 0.0, 8.431501819999987, 20.136762988, 46.346144854, 49.27723979200002, 13.92279254799998, 17.399880168000017, 1.775952328000017, 0.0, 0.0, 100.05095278399997, 10.093222958000005, 11.773899312000005, 1.6437990420000048, 39.870625812, 0.0, 18.060582689999993, 8.934279671999992, 37.41986883199999, 15.912094182, 5.966114200000003, 30.28164020399998, 47.322400784, 37.080793428000014, 47.22883371599999, 17.785042666000006, 26.83582321199999, 18.32636537400001, 30.341216415999988, 17.182806064000005, 0.0, 58.09183862800001, 36.14568290800001, 2.7136241720000065, 86.40157097399998, 19.611504443999994, 66.233864472, 116.53113707399999, 78.727627266, 214.64939716799992, 15.270879934000003, 110.63334480000002, 41.02786223999999, 33.08275428799998, 50.112958952, 69.570522678, 103.03021164, 22.830805840000004]        
        student_output = wait_a_bit(water_level, water_level_loss_no_prevention, water_level_loss_with_prevention)

        self.assertIsNotNone(student_output, "wait_a_bit() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected wait_a_bit() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected wait_a_bit() to return list of length {len(expected_output)}. Got {len(student_output)}")
        
        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For wait_a_bit(), for year {2020+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")

    def test_part_2_2c_prepare_immediately(self):
        np.random.seed(0)
        random.seed(0)

        water_level_loss_with_prevention = np.array([[5,6,7,8,9,10],[0,5,15,30,70,100]]).T

        water_level = [4.4181169189, 4.2432523603, 4.3706582199, 4.6214625724, 4.5992644453, 4.1217571709, 4.5090599508, 4.3305540324, 4.36929164, 4.5048728959, 4.4806502956, 4.8077094626, 4.6958176721, 4.5842193972, 4.7006383708, 4.7112153245, 5.0596676552, 4.6382490475, 4.8194558746, 4.5131621302, 4.0239461998, 5.0466333831, 5.1637915421, 4.667325595, 5.7603494416, 4.4694850712, 5.057247906, 5.0071681917, 5.7350299728, 5.7674485578, 5.2659409422, 5.4116822033, 4.8851984421, 4.4017149723, 5.2107875455, 5.5034190747, 6.1057690809, 6.1546206632, 5.3480698137, 5.4349970042, 5.0443988082, 4.8532731338, 4.7026613805, 7.0006369098, 5.5046611479, 5.5886949656, 5.0821899521, 6.4967656453, 4.8816427442, 5.9030291345, 5.4467139836, 6.4354967208, 5.7956047091, 5.29830571, 6.2570410051, 6.6830600196, 6.4270198357, 6.6807208429, 5.8892521333, 6.1708955803, 5.9163182687, 6.2585304104, 5.8591403032, 4.9780687254, 6.9522959657, 6.4036420727, 5.1356812086, 7.4400261829, 5.9805752222, 7.1038977412, 7.9421856179, 7.3121271211, 8.5915587323, 5.7635439967, 7.84388908, 6.525696556, 6.3270688572, 6.7528239738, 7.1595087113, 7.717170194, 6.070770146]

        expected_output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.1933531040000034, 0.0, 0.0, 0.0, 0.0, 0.9326676619999928, 3.275830842000005, 0.0, 15.206988831999995, 0.0, 1.1449581199999948, 0.14336383399999875, 14.70059945599999, 15.348971155999996, 5.318818844000006, 8.233644065999997, 0.0, 0.0, 4.2157509099999935, 10.068381494, 24.230763236, 26.18482652800001, 6.96139627399999, 8.699940084000009, 0.8879761640000084, 0.0, 0.0, 60.03821458799998, 10.093222958000005, 11.773899312000005, 1.6437990420000048, 39.870625812, 0.0, 18.060582689999993, 8.934279671999992, 37.41986883199999, 15.912094182, 5.966114200000003, 30.28164020399998, 47.322400784, 37.080793428000014, 47.22883371599999, 17.785042666000006, 26.83582321199999, 18.32636537400001, 30.341216415999988, 17.182806064000005, 0.0, 58.09183862800001, 36.14568290800001, 2.7136241720000065, 86.40157097399998, 19.611504443999994, 66.233864472, 116.53113707399999, 78.727627266, 214.64939716799992, 15.270879934000003, 110.63334480000002, 41.02786223999999, 33.08275428799998, 50.112958952, 69.570522678, 103.03021164, 22.830805840000004]        
        student_output = prepare_immediately(water_level, water_level_loss_with_prevention)

        self.assertIsNotNone(student_output, "prepare_immediately() returned None instead of a list!")
        self.assertTrue(type(student_output)==type(expected_output), f"Expected prepare_immediately() to return {type(expected_output)}. Got {type(student_output)}")
        self.assertEqual(len(expected_output), len(student_output), f"Expected prepare_immediately() to return list of length {len(expected_output)}. Got {len(student_output)}")
        
        epsilon = 1e-2

        for i in range(len(expected_output)):
            self.assertAlmostEqual(expected_output[i], student_output[i], delta=epsilon, msg=f"For prepare_immediately(), for year {2020+i}, expected damage costs of {expected_output[i]}. Got {student_output[i]}")


# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
    'test_part_1_1_predicted_sea_level_rise': 1,
    'test_part_1_2_simulate_year_1': 0.5,
    'test_part_1_2_simulate_year_2': 0.5,
    'test_part_2_1_simulate_water_levels': 1,
    'test_part_2_2a_repair_only': 0.33,
    'test_part_2_2b_wait_a_bit': 0.33,
    'test_part_2_2c_prepare_immediately': 0.34
}

class Results_600(unittest.TextTestResult):
    # We override the init method so that the Result object can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = sum(point_values.values())
        self.total_points = sum(point_values.values())

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points

    def getTotalPoints(self):
        return self.total_points


if __name__=="__main__":
    try:
        STUDENT_KERBEROS = sys.argv[1]
    except IndexError as e:
        STUDENT_KERBEROS = ''
    print("Running unit tests for student %s" % STUDENT_KERBEROS)

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS4))
    result = unittest.TextTestRunner(verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = result.getPoints()

    # weird bug with rounding
    if points < .1:
        points = 0

    print("\nProblem Set 4 Unit Test Results:")
    print(output)
    print(f"Points: {points}/{result.getTotalPoints()}\n")
