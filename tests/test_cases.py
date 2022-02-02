import unittest
import os
from util4tests import run_single_test, log

from xmlasdict import parse


class TestBasicCases(unittest.TestCase):

    def test_simple(self):
        log.info("test simple")
        xmlinfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '01-basic.xml')
        xml = parse(xmlinfile)

    def test_lists(self):
        # should make lists of repeating children
        pass

    def test_roundtrip(self):
        # check if xml output is same after reading and re-serializing
        pass


    def test_reordering(self):
        # check effect of <group><a/><b/><a/><b/></group> --> .a and .b should yield two lists
        pass

    def test_mixed_content_model(self):
        # and difference between innerXML versus text() node
        pass

    def test_whitespace(self):
        # check expectations (if any concerning whitespace)
        """ what is same and what is different between
        <root><row><x>1</x></row></root>
          and

        <root><row><x> 1 </x></row></root>

         and
        <root>
          <row>
            <x>
              1
            </x>
          </row>
        </root>
        """
        pass

    def test_attributes(self):
        # check addressing test_attributes
        pass

    def test_namespaces(self):
        # check what to do about namespace declarations and prefixes
        pass



if __name__ == "__main__":
    run_single_test(__file__)
