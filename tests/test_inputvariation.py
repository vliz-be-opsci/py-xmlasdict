import gzip
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

    # in lxml (https://lxml.de/lxmlhtml.html)
    #  TODO make these work also
    def test_url_input(self):
        urlwithxml = "https://example.org/xml-document"
        # xml = parse(urlwithxml) #((should check Doctype definition (if provided) or <>))
        # assert xml is not None, "we should have gotten some return"

    # in xml.etree (https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.fromstringlist)
    def test_sequence_input(self):
        sequenceObj = ["<root>", "<nested>something</nested>", "</root>"]  # TODO check for actual examples
        # xml = parse(sequenceObj)
        # assert xml is not None, "we should have gotten some return"

    #### other ways, probably not necessary ####
    # iter mode --> from xml.etree (https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.iterparse)
    def test_iterparse_input(self):
        pass

    # streaming mode --> from xmltodict (https://github.com/martinblech/xmltodict)
    # xmltodict.parse(GzipFile('somegzippedxmlfile.xml.gz'), item_depth=2, item_callback=some_callbackfunction_to_handle_specificElements)
    def test_streaming_input(self):
        pass


if __name__ == "__main__":
    run_single_test(__file__)
