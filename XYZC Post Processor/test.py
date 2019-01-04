import unittest
from calc import G2_G3_values
from calc import origin_xy



class TestCalc(unittest.TestCase):
    def test_G2_G3_values(self):

        self.assertEqual(G2_G3_values("G2 X  3.354 Y  3.354 I  0.354 J  0.354"), (3.354, 3.354, 0.354, 0.354))

    def test_origin_xy(self):
        self.assertEqual(origin_xy(1,1,1,1),(2,2))


    def test_vectors(self):
        self.assertEqual(vectors(x_1, y_1, x_2, y_2, origin_x, origin_y),(VEC_1x, VEC_1y, VEC_2x, VEC_2y))

    def test_dot(self):
        self.assertEqual(dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y),dotprod)

    def test_magnitude(self):
        self.assertEqual(magnitude(VEC_1x, VEC_1y, VEC_2x, VEC_2y),magnitude)

    def multi_mag(self):
        self.assertEqual(multi_mag(mag_1, mag_2),())

if __name__ == '__main__':
    unittest.main()