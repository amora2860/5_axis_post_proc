import unittest
from calc import *



class TestCalc(unittest.TestCase):
    def test_G2_G3_values(self):

        self.assertEqual(G2_G3_values("G3 X  16.939 Y  10.672 I  -1.000 J   0.000"), (16.939, 10.672, -1.000, 0.000))

    def test_origin_xy(self):
        self.assertEqual(origin_xy(1,1,1,1),(2,2))

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



if __name__ == '__main__':
    unittest.main()