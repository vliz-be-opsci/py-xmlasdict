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

    def test_attributes(self):
        # check addressing test_attributes
        xdict = parse("<r top='me'><child type='some'/></r>")
        assert xdict['@top'] == 'me', "error accessing root attribute"
        assert xdict.child['@type'] == 'some', "error accessing child attribute"

    def test_list_access(self):
        xdict = parse("<r a='on'><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d></r>")

        # basic roundtrip support like innerXML
        assert str(xdict) == '<i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d>'

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

        # and a choice in referencing syntax
        log.debug(f"type(xdict)={type(xdict)}")
        log.debug(f"xdict.i={xdict.i}")
        log.debug(f"xdict['i']={xdict['i']}")
        assert str(xdict.i) == str(xdict['i']), "referencing childs should be supported in two ways"
        assert len(xdict.i) == len(xdict['i']), "referencing childs should be supported in two ways"
        # todo implement __hash__ and __eq__ on wrapper and iterwrapper for this to work!
        # assert xdict.i == xdict['i'], "referencing childs should be supported in two ways"

    def test_dict_ness(self):
        # there is also some more dictlike behaviour we expose
        xdict = parse("<r a='on'><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d></r>")
        assert set(xdict) == {'i', 's', 'd', '@a'}, "iterating the xdict should expose its keys()"

        assert len(list(xdict)) == 4, "not the order but the size should be predictable"

        pydict = dict(xdict)
        assert set(xdict) == set(pydict), "the sets of keys should match"
        assert str(pydict['i']) == "['1', '2', '3']"
        assert [int(str(n)) for n in pydict['i']] == [1, 2, 3]
        assert str(pydict['s']) == "['a', 'b', 'c']"
        assert [str(n) for n in pydict['s']] == ['a', 'b', 'c']
        assert str(pydict['d']) =='<n>me</n>'

    def test_list_all(self):
        # there is also a way to just iterate over all the nested children
        xdict = parse("<r a='on'><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d></r>")
        assert [str(x) for x in xdict['*']] == ['1', '2', 'a', '3', 'b', 'c', '<n>me</n>']
        assert [x.tag for x in xdict['*']] == ['i', 'i', 's', 'i', 's', 's', 'd']
        assert xdict['*'].tag == ['i', 'i', 's', 'i', 's', 's', 'd']

    def test_empty(self):
        # we should decide how <empty/> elements should be read
        xdict = parse("<root><empty type='important' /></root>")
        assert str(xdict.empty) == '', "empty elements should produce empty string representation"
        assert not(bool(xdict.empty)), "empty elements should behave as false"

    def test_unpack_shallow(self):
        # should allow automatic unpacking of lead-wrappers down to the level of naked rows
        # NOTE pysubyt does this for xml sources so we will need this
        xdict = parse("<r0><r1><r2><r3><d>1</d><d>2</d></r3></r2></r1></r0>")
        data = xdict.unpack()
        log.debug(f"data = {data} type = {type(data)}")
        assert data.dumps() == "<d>1</d><d>2</d>"
        assert str(data) == "['1', '2']"

        # todo find a way to automatically dig down to the level of the first list like pysubyt does --> ie down to ro.r1.r2.r3
        xdict = parse("<r0><r1><r2><r3><d>1</d></r3></r2></r1></r0>")
        data = xdict.unpack()
        assert data.dumps() == "<d>1</d>"
        assert str(data) == "1"

    def test_unpack_deep(self):
        # should allow automatic unpacking of lead-wrappers down to the level of naked rows
        # NOTE pysubyt does this for xml sources so we will need this
        xdict = parse("<r0><r1><r2><r3><d><id>1</id><nm>Me</nm></d><d><id>2</id><nm>You</nm></d></r3></r2></r1></r0>")
        data = xdict.unpack()
        assert data.dumps() == "<d><id>1</id><nm>Me</nm></d><d><id>2</id><nm>You</nm></d>"
        assert [str(n) for n in data] == ['<id>1</id><nm>Me</nm>', '<id>2</id><nm>You</nm>']

        # todo find a way to automatically dig down to the level of the first list like pysubyt does --> ie down to ro.r1.r2.r3
        xdict = parse("<r0><r1><r2><r3><d><id>1</id><nm>One</nm></d></r3></r2></r1></r0>")
        data = xdict.unpack()
        assert data.dumps() == "<d><id>1</id><nm>One</nm></d>"
        assert [str(n) for n in data] == ['<id>1</id><nm>One</nm>']

    def test_roundtrip(self):
        inputs = [
            """<some><content>text</content><empty /></some>""",
        ]

        for xml in inputs:
            xdict = parse(xml)
            assert xdict.dumps() == xml, f"failed roundtrip parse-serialize for {xml}"

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

    def test_namespaces(self):
        # check what to do about namespace declarations and prefixes

        # xdict = parse("""<root xmlns="https://example.org/p1 xmlns:pfx="https://example.org/p2">
        #  <a xmlns="https://example.org/p1">a in p1</a>
        #  <pfx:a>a in p2</pfx:a>
        # </root>""", dict(p1="https://example.org/p1", p2="https://example.org/p2"))

        # assert str(xdict['p1:a']) == 'a in p1'
        # assert str(xdict['p2:a']) == 'a in p1'
        # assert str(xdict.a) == ??
        # assert str(xdict['a']) == ??

        # inspiration:
        # https://github.com/martinblech/xmltodict#namespace-support
        # https://github.com/martinblech/xmltodict/blob/master/tests/test_xmltodict.py#L182 (tests)
        # https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
        # https://github.com/python/cpython/blob/3.10/Lib/test/test_xml_etree.py#L1161 (tests)
        pass

if __name__ == "__main__":
    run_single_test(__file__)
