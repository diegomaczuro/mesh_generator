# -*- coding: utf_8 -*-
import unittest
import numpy as np
from framework2.interpolation import alg_interp
from framework2.model import *

class MyTestCase(unittest.TestCase):

    def assertAlmostListEqual(self, l1, l2):

        self.assertEqual(len(l1), len(l2))

        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i])

    def assertAlmostDictEqual(self, d1, d2):

        self.assertEqual(len(d1), len(d2))

        for k in d1.keys():
            self.assertAlmostEqual(d1[k], d2[k])

    def test_load(self):
        md = ModelData('test.csv')
        MODEL_NUM = 0
        model_data = md.data[md.data.model_num == MODEL_NUM].R_ep2

        self.assertEqual(24, len(model_data.index))
        self.assertEqual(24, len(model_data.values))

    def test_interp(self):
        a, b, c, d = alg_interp([0, np.pi / 2, np.pi, 2 * np.pi], [1, 2, 3.5, 1])

        self.assertAlmostListEqual([          1,           2,         3.5,  1.], a)
        self.assertAlmostListEqual([ 0.56742197,  0.77501538, -0.96184944,  0.], b)
        self.assertAlmostListEqual([ 0.        ,  0.13215807,  0.07929484,  0.], c)
        self.assertAlmostListEqual([ 0.02804481, -0.01121793, -0.00841344,  0.], d)

    def test_interpolate(self):
        md = ModelData('test.csv')

        params1 = md.params(0)
        params2 = md.params(10000)

        self.assertAlmostDictEqual(params1, params2)


if __name__ == '__main__':
    unittest.main()
