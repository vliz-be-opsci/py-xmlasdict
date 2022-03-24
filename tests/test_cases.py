import unittest
from util4tests import run_single_test, log
from xmlasdict import parse


class TestCases(unittest.TestCase):

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
        assert str(pydict['d']) == '<n>me</n>'

    def test_unwrap(self):
        xdict = parse("<r p='@p'><a>a</a><a><aa>aa</aa><ab>ab</ab></a><b>b</b></r>")
        shallow_dict = dict(xdict)
        assert [str(n) for n in shallow_dict['a']] == ['a', '<aa>aa</aa><ab>ab</ab>']

        assert xdict.unwrap() == {'@p': '@p', 'a': ['a', {'aa': 'aa', 'ab': 'ab'}], 'b': 'b'}
        assert xdict['*'].unwrap() == ['a', {'aa': 'aa', 'ab': 'ab'}, 'b']
        assert xdict['a'].unwrap() == ['a', {'aa': 'aa', 'ab': 'ab'}]
        assert xdict['b'].unwrap() == 'b'
        assert xdict['.//aa'].unwrap() == 'aa'

    def test_list_all(self):
        # there is also a way to just iterate over all the nested children
        xdict = parse("<r a='on'><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d></r>")
        assert [str(x) for x in xdict['*']] == ['1', '2', 'a', '3', 'b', 'c', '<n>me</n>']

    def test_path_like_access(self):
        # there is also a way to just iterate over all the nested children
        xdict = parse("<r><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><s>me</s></d></r>")
        assert [str(n) for n in xdict['s']] == ['a', 'b', 'c']
        assert [str(n) for n in xdict['./s']] == ['a', 'b', 'c']
        assert [str(n) for n in xdict['.//s']] == ['a', 'b', 'c', 'me']
        assert str(xdict['d/s']) == 'me'
        assert str(xdict['./d/s']) == 'me'
        assert str(xdict['.//d/s']) == 'me'

    def test_tag_getting(self):
        xdict = parse("<r a='on'><i>1</i><i>2</i><s>a</s><i>3</i><s>b</s><s>c</s><d><n>me</n></d></r>")
        assert [x.tag for x in xdict['*']] == ['i', 'i', 's', 'i', 's', 's', 'd']
        assert xdict['*'].tag == ['i', 'i', 's', 'i', 's', 's', 'd']

    def test_ambiguous_terms(self):
        known_members = ['tag', 'dumps', 'unpack', 'unwrap']
        xml = "<r>" + "".join([f"<{m}>{m}_content</{m}>" for m in known_members]) + "</r>"
        # we have to be cautious with the introduced functions and properties as they hide some potential tags
        xdict = parse(xml)
        # tag
        assert xdict.tag == 'r'
        assert str(xdict['tag']) == 'tag_content'
        # dumps
        assert xdict.dumps() == xml
        assert str(xdict['dumps']) == 'dumps_content'
        # unpack
        assert xdict.unpack()[0] == xdict
        assert str(xdict['unpack']) == 'unpack_content'
        # unwrap
        assert xdict.unwrap()['unwrap'] == 'unwrap_content'
        assert str(xdict['unwrap']) == 'unwrap_content'

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
        mixed_content = '<a href="http://example.org/">This</a> is <em>actual</em> mixed <strong>content</strong>'
        mixed_xml = "<p>" + mixed_content + "</p>"
        xdict = parse(mixed_xml)
        assert str(xdict) == mixed_content
        assert xdict.dumps() == mixed_xml

    def test_ignore_whitespace(self):
        # three variants of the same xml -- and how xdict handles them
        strict = "<root><row><x>1</x></row></root>"
        spaced = "<root><row><x> 1 </x></row></root>"
        pretty = """<root>
          <row>
            <x>
              1
            </x>
          </row>
        </root>"""

        strict_xdict = parse(strict)
        spaced_xdict = parse(spaced)
        pretty_xdict = parse(pretty)

        #  roundtripping keeps all whitespace
        assert strict_xdict.dumps() == strict
        assert spaced_xdict.dumps() == spaced
        assert pretty_xdict.dumps() == pretty

        # but value access is stripped
        assert f"{strict_xdict.row.x}" == f"{spaced_xdict.row.x}"
        assert f"{strict_xdict.row.x}" == f"{pretty_xdict.row.x}"

    def test_list_enforcing(self):
        """ Specific test for [issue #4](https://github.com/vliz-be-opsci/py-xmlasdict/issues/4)
        """
        xmlmulti = """
            <rows>
                <item a="A1"><b>B1</b><c>C1</c></item>
                <item a="A2"><b>B2</b><c>C2</c></item>
            </rows>
        """
        xmlsingle = """
            <rows>
                <item a="A1"><b>B1</b><c>C1</c></item>
            </rows>
        """
        xmlnone = """
            <rows>
                <no_item_here />
            </rows>
        """
        xmls = dict(multi=xmlmulti, single=xmlsingle, none=xmlnone)
        expected_count = len(xmls)
        for name, xml in xmls.items():
            expected_count -= 1
            xdict = parse(xml)  # parse(xml.strip())
            count = 0
            for item in xdict['item[]']:
                count += 1
                assert item.tag == 'item', f"wrong tag in case {name}"
            assert count == expected_count, f"wrong count in case {name}"

    def test_unpack_limiting(self):
        """ Specific test for [side-issue of #4](https://github.com/vliz-be-opsci/py-xmlasdict/issues/4)
        """
        xml = "<root><wrap><item><name>Me</name></item></wrap></root>"
        xdict = parse(xml)

        assert xdict.tag == 'root'
        lowest = xdict.unpack()
        for n in lowest:
            assert n.tag == 'name'
        targetted = xdict.unpack(tag='item')
        for t in targetted:
            assert t.tag == 'item'

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
