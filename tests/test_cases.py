import unittest
from util4tests import run_single_test, log

from xmlasdict import MyModel, log


class TestBasicCases(unittest.TestCase):

    def test_simple(self):
        xmlinfile = "todo"
        log.info("testing str.upper()")
        self.assertEqual('foo'.upper(), 'FOO')



if __name__ == "__main__":
    run_single_test(__file__)
