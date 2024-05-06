import unittest
import math

from main import calculate_distance, calculate_ppi, calculate_real_world_distance
#UINT TESTING 

class TestCalculateDistance(unittest.TestCase):

    def test_calculate_distance(self):
        # Test case 1: (x1, y1) = (0, 0), (x2, y2)  HAZEM
        self.assertAlmostEqual(calculate_distance(288.64, 234.63, 419.07, 228.20), 130.58, places=1)

        # Test case 2: (x1, y1) = (-1, -1), (x2, y2)  OMAR
        self.assertAlmostEqual(calculate_distance(200.76, 175.26, 316.57, 178.80), 115.86, places=1)

        # Test case 3: (x1, y1) = (5, 5), (x2, y2) MOAEEAD
        self.assertAlmostEqual(calculate_distance(243.14, 294.38, 342.13, 293.97), 98.98, places=1)
    #-------------------------------------------------------------------------    
    def test_calculate_ppi(self):
        # Test case 1: HAZEM
        self.assertAlmostEqual(calculate_ppi(1096.0, 172.0), 16.18, places=1)

        # Test case 2: OMAR
        self.assertAlmostEqual(calculate_ppi(1227.0, 179.0), 17.41, places=1)

        # Test case 3: MOAEEAD
        self.assertAlmostEqual(calculate_ppi(1016.0, 167.0), 15.45, places=1)
    #-------------------------------------------------------------------------    
    def test_calculate_real_world_distance(self):
        # Test case 1: pixel_distance HAZEM
        self.assertAlmostEqual(calculate_real_world_distance(101.73, 16.18), 15.96, places=1)

        # Test case 2: pixel_distance OMAR
        self.assertAlmostEqual(calculate_real_world_distance(115.86, 17.41), 16.90, places=1)

        # Test case 3: pixel_distance MOAEEAD
        self.assertAlmostEqual(calculate_real_world_distance(98.98, 15.45), 16.27, places=1)
        
if __name__ == '__main__':
    unittest.main()
