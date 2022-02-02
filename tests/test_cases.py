import unittest
import os
from util4tests import run_single_test, log

from xmlasdict import parse


class TestBasicCases(unittest.TestCase):

    def test_basic_file(self):
        log.info("test simple")
        xmlinfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '01-basic.xml')
        xdict = parse(xmlinfile)
        # TODO make actually some predictions based on that sample file

    def test_access(self):
        xdict = parse("<root><num>1</num><name>Marc</name></root>")
        #assert xdict.num == '1', "error accessing first node"
        #assert xdict.name == Name, "error accessing second node"


    def test_lists(self):
        # should make lists of repeating children
        pass

    def test_iteration(self):
        # should allow running through all the keys (i.e. child-elements and attributes)
        pass

    def test_roundtrip(self):
        inputs = [
            """<some><content>text</content><empty /></some>"""
        ]

        for xml in inputs:
            xdict = parse(xml)
            assert str(xdict) == xml, f"failed roundtrip parse-serialize for {xml}"


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
