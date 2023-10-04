import unittest

import numpy as np
from scipy import integrate

import ece3210_lab01
import ece3210_lab01_sol


class TestCircuit(unittest.TestCase):

    def test_py(self):

        array_size = 10000
        t = np.sort(np.random.uniform(low=-5,high=5,
                                      size=array_size))

        # t = np.linspace(0,10,array_size)
        f = np.random.normal(5,0.5,
                             size=array_size)
        
        y_py, y_t_py = ece3210_lab01.py_cumtrapz(f, t)

        y_sol, y_t_sol = ece3210_lab01_sol.cumtrapz(f, t)
        
        np.testing.assert_array_almost_equal(y_py,
                                             y_sol)
        
        np.testing.assert_array_almost_equal(y_t_py,
                                             y_t_sol)

    def test_value_error_py(self):
        t = np.linspace(0, 10, 99)
        f = np.linspace(0, 10, 100)

        with self.assertRaises(ValueError):
            ece3210_lab01.py_cumtrapz(f,t)

        
    def test_c(self):

        array_size = 10000
        t = np.sort(np.random.uniform(low=-5,high=5,
                                      size=array_size))

        f = np.random.normal(5,0.5,
                             size=array_size)
        
        y_py, y_t_py = ece3210_lab01.c_cumtrapz(f, t)

        y_sol, y_t_sol = ece3210_lab01_sol.cumtrapz(f, t)
        
        np.testing.assert_array_almost_equal(y_py,
                                             y_sol)
        
        np.testing.assert_array_almost_equal(y_t_py,
                                             y_t_sol)


    def test_value_error_c(self):
        t = np.linspace(0, 10, 99)
        f = np.linspace(0, 10, 100)

        with self.assertRaises(ValueError):
            ece3210_lab01.c_cumtrapz(f,t)

            
if __name__ == '__main__':
    unittest.main()




