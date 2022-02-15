import unittest
import os
from xmlasdict import parse
from util4tests import run_single_test


class TestSettings(unittest.TestCase):

    def test_fitness(self):
        fitnessfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '02-fitness.xml')
        _ = parse(fitnessfile)       
        
        assert f"{_.A}" == ""
        
        pass
        
        



if __name__ == '__main__':
    run_single_test(__file__)
