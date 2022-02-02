import unittest
import os
from util4tests import run_single_test, log

from xmlasdict import parse


class TestBasicCases(unittest.TestCase):

    def test_basic_file(self):
        xmlinfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '01-basic.xml')
        xdict = parse(xmlinfile)
        # TODO make actually some predictions/tests based on the content of that sample file

    def test_access(self):
        xdict = parse("<root><num>1</num><name>Marc</name></root>")
        assert int(str(xdict.num)) == 1, "error accessing num node content"
        assert str(xdict.name) == 'Marc', "error accessing name node content"

    def test_nested_access(self):
        xdict = parse("<root><wrap><num>1</num><name>Marc</name></wrap></root>")
        assert int(str(xdict.wrap.num)) == 1, "error accessing num node content"
        assert str(xdict.wrap.name) == 'Marc', "error accessing name node content"

    def test_list_access(self):
        # should make lists of repeating children
        xdict = parse("<r><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s></r>")
        # assert list(xdict.i) == ['1', '2', '3']
        # assert list(xdict.s) == ['a', 'b', 'c']
        # assert xdict.i[0] == '1'
        pass

    def test_list_iteration(self):
        # should allow to for-next over values in recurring child-elements
        # actually -- also if one loops over a single occurence !!!
        pass

    def test_empty(self):
        # we should decide how <empty/> elements should be read
        pass

    def test_inspection(self):
        # should allow running through all the keys (i.e. child-elements and attributes)
        pass


    def test_unpack(self):
        # should allow automatic unpacking of lead-wrappers down to the level of naked rows
        # NOTE pysubyt does this for xml sources so we will need this
        pass

    def test_roundtrip(self):
        inputs = [
            """<some><content>text</content><empty /></some>""",
        ]

        for xml in inputs:
            xdict = parse(xml)
            assert xdict.dumps() == xml, f"failed roundtrip parse-serialize for {xml}"

    def test_reordering(self):
        # check effect of <group><a/><b/><a/><b/></group> --> .a and .b should yield two lists
        pass

    def test_mixed_content_model(self):
        # and difference between innerXML versus text() node ???
        pass

    def test_whitespace(self):
        # check expectations (if any) concerning whitespace
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
        xdict = parse("<r top='me'><child type='some'/></r>")
        assert xdict['@top'] == 'me', "error accessing root attribute"
        assert xdict.child['@type'] == 'some', "error accessing child attribute"

    def test_namespaces(self):
        # check what to do about namespace declarations and prefixes
        pass


if __name__ == "__main__":
    run_single_test(__file__)
