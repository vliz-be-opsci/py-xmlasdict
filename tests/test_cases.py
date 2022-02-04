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

        # one is expected to iterate lists
        assert list(int(str(i)) for i in xdict.i) == [1, 2, 3]
        assert list(str(s) for s in xdict.s) == ['a', 'b', 'c']

        # but we also assure a nice unwrapped direct str representation
        assert (str(xdict.i)) == "['1', '2', '3']"
        log.debug(f"xdict.i = {xdict.i}")
        log.debug(f"type(xdict.i) = {type(xdict.i)}")

        # as well as direct subscripting by index and slice
        assert int(str(xdict.i[0])) == 1
        assert str(xdict.i[1:]) == "['2', '3']"

        # can we expect this in the case of list(xdict)?
        # assert list(xdict) == ['<i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s>', '1', '2', 'a', '3', 'b', 'c']
        # remarks (mpo) --
        #   if useful, then probably without the first 'self' included in the list, but just an iteration of all nested children
        #   and finally - list() will give us no opportunity to unwrap - so one will at least need to iterate the list, not just wrap it!
        #   NOTE: this view also brings an extra challenge in combo with mixed content model --> top level text-nodes ?

    def test_list_iteration(self):
        # should allow to for-next over values in recurring child-elements
        xdict = parse("<r><i>1</i><s>a</s><i>2</i><s>b</s></r>")
        # iter_xdict = iter(xdict)
        # next_element = next(iter_dict)
        # assert str(next_element) = '<i>1</i><i>2</i><s>a</s><s>b</s>'
        # assert list(next_element.i) = ['1','2']

        # actually -- also if one loops over a single occurence !!!
        # iter_xdict_i = iter(xdict.i)
        # assert str(next(iter_xdict_i)) = '1'
        # assert str(next(iter_xdict_i)) = '2'

        # iter_xdict_s = iter(xdict.s)
        # assert list(iter_xdict_s) = ['a', 'b']
        pass

    def test_empty(self):
        # we should decide how <empty/> elements should be read
        xdict = parse("<root><empty type='important'></empty></root>")
        # Option 1: return them as an empty string -> not desirable in templates
        # assert str(xdict.empty) == ''
        # Option 2 (if possible): make str/text representation a null object OR false
        # assert xdict.empty != null
        # assert str(xdict.empty) == null
        #  remarks (mpo)
        #     -- null not a python concept --> None?
        #     -- False feels arbitrary --> actually why not "True" as indication of the existence/presence of the element?
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
        # inspiration: 
        # https://github.com/martinblech/xmltodict#namespace-support 
        # https://github.com/martinblech/xmltodict/blob/master/tests/test_xmltodict.py#L182 (tests)
        # https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
        # https://github.com/python/cpython/blob/3.10/Lib/test/test_xml_etree.py#L1161 (tests)
        pass


if __name__ == "__main__":
    run_single_test(__file__)
