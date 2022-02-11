import unittest
import os
from util4tests import run_single_test

from xmlasdict import parse


class TestBasicFile(unittest.TestCase):

    def test_basic_file(self):
        xmlinfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '01-basic.xml')
        xdict = parse(xmlinfile)
        assert f"{xdict.someabstract.para}" == 'This line contains something unusual'
        assert f"{xdict.someLicense.para}" == ''.join([
            'This work is licensed under a ',
            '<ulink url="http://creativecommons.org/licenses/by/4.0/legalcode">',
            '<citetitle>Creative Commons Attribution (CC-BY) 4.0 License</citetitle>',
            '</ulink>.'])
        assert f"{xdict.someLicense.para.ulink['@url']}" == 'http://creativecommons.org/licenses/by/4.0/legalcode'
        ct = xdict['.//citetitle']
        assert ct.dumps() == '<citetitle>Creative Commons Attribution (CC-BY) 4.0 License</citetitle>'
        assert f"{ct}" == 'Creative Commons Attribution (CC-BY) 4.0 License'


if __name__ == "__main__":
    run_single_test(__file__)
