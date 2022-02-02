import unittest
from util4tests import run_single_test, log
import os

from xmlasdict import parse


class TestInputVariants(unittest.TestCase):

    def test_file_input(self):
        xmlinfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '01-basic.xml')
        xml = parse(xmlinfile)
        assert xml is not None, "we should have gotten some return"

    def test_string_input(self):
        xml = parse("<root/>")
        assert xml is not None, "we should have gotten some return"

    def test_other_input(self):
        # TODO check with xmltodict what support they have + als check with emltree of course
        pass


if __name__ == "__main__":
    run_single_test(__file__)
