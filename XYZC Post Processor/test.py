import unittest
from calc import *



class TestCalc(unittest.TestCase):
    def test_G2_G3_values(self):
        self.assertEqual(G2_G3_values("G2 X  2.000 Y  3.000 I  0.750 J -0.250"),(2.00, 3.0, 0.75, -0.25))

    def test_origin_xy(self):
        self.assertEqual(origin_xy(0.5, 3.0, 0.75, -0.25),(1.25,2.75))

    def test_vectors_G2_G3(self):
        self.assertEqual(vectors_G2_G3(0.5, 3.0, 2.0, 3.0, 1.25, 2.75),(0.75, -0.25, -0.75, -0.25))

    #the result is zero which is not right.
    def test_dot(self):
        self.assertEqual(dot(0.75, -0.75, -0.25, -0.25 ), (-0.5))

    def test_magnitude(self):
        self.assertEqual(magnitude(0.75, -0.25, -0.75, -0.25), (0.7905694150420949, 0.7905694150420949))

    def test_multi_mag(self):
        self.assertEqual(multi_mag(0.7905694150420949, 0.7905694150420949),(0.6250000000000001))

    def test_rads(self):
        self.assertEqual(rads(-0.5, 0.6250000000000001),(2.4980915447965084))

    def test_arc_cords_p1(self):
        self.assertEqual(arc_cords_p1(x_1, y_1, origin_x, origin_y, theta),())

    def test_arc_cords_p2(self):
        self.assertEqual(arc_cords_p2(x_2, y_2, origin_x, origin_y, theta),())

    def test_arc_comp(self):
        self.assertEqual(arc_comp(cord_p1, cord_p2, G_code),())

    def test_starting_c_pos(self):
        self.assertEqual(starting_c_pos(cord_p1, G_code),())


#this section tests out the G0 & G1 commands
    def test_C_G0_G1_eval(self):
        # Test for straight line
        self.assertEqual(C_G0_G1_eval("G1 X  0.500 Y  3.000",0.5, 0.5),(0.0))
        self.assertEqual(C_G0_G1_eval("G1 X  2.500 Y  1.000", 2.0, 1.5), (135.0))

    def test_arc_cords_p1(self):
        self.assertEqual(arc_cords_p1(1, -1, 0, 0), ("1"))
        self.assertEqual(arc_cords_p1(1, 1, 0, 0),("2"))
        self.assertEqual(arc_cords_p1(-1, 1, 0, 0), ("3"))
        self.assertEqual(arc_cords_p1(-1, -1, 0, 0),("4"))
        self.assertEqual(arc_cords_p1(1, 0, 0, 0), ("1&2"))
        self.assertEqual(arc_cords_p1(0, 1, 0, 0), ("2&3"))
        self.assertEqual(arc_cords_p1(-1, 0, 0, 0), ("3&4"))
        self.assertEqual(arc_cords_p1(0, -1, 0, 0), ("1&4"))

    # finds the cordinate that point #2 is in
    def test_arc_cords_p2(self):
        self.assertEqual(arc_cords_p2(1, -1, 0, 0), ("1"))
        self.assertEqual(arc_cords_p2(1, 1, 0, 0),("2"))
        self.assertEqual(arc_cords_p2(-1, 1, 0, 0), ("3"))
        self.assertEqual(arc_cords_p2(-1, -1, 0, 0),("4"))
        self.assertEqual(arc_cords_p2(1, 0, 0, 0), ("1&2"))
        self.assertEqual(arc_cords_p2(0, 1, 0, 0), ("2&3"))
        self.assertEqual(arc_cords_p2(-1, 0, 0, 0), ("3&4"))
        self.assertEqual(arc_cords_p2(0, -1, 0, 0), ("1&4"))

    def test_eval2_theta(self):
        #cordinate #1 with (y_2 < y_3) (G2)
        self.assertEqual(eval2_theta("1", 1, -1, 0, 0, 5, -8, 30, "G2"),(30))
        # cordinate #1 with (y_2 < y_3) (G3)
        self.assertEqual(eval2_theta("1", 1, -1, 0, 0, 5, -8, 30, "G3"), (330))

         #cordinate #1 with (y_2 > y_3) (G2)
        self.assertEqual(eval2_theta("1", 1, -1, 0, 0, 5, -0.5, 30, "G2"),(330))
        # cordinate #1 with (y_2 > y_3) (G3)
        self.assertEqual(eval2_theta("1", 1, -1, 0, 0, 5, -0.5, 30, "G3"), (30))

        # cordinate #2 with (y_2 > y_3) (G2)
        self.assertEqual(eval2_theta("1", 1, 1, 0, 0, 5, 8, 30, "G2"), (330))
        # cordinate #2 with (y_2 > y_3) (G2)
        self.assertEqual(eval2_theta("1", 1, -1, 0, 0, 5, 0.5, 30, "G2"), (330))



    def test_C_G2_G3_eval(self):
        self.assertEqual(C_G2_G3_eval("G2 X  2.000 Y  3.000 I  0.750 J -0.250", "G2"),(10))

if __name__ == '__main__':
    unittest.main()