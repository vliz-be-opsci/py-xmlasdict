from collections.abc import Mapping
from xml.etree import ElementTree
import logging


log = logging.getLogger(__name__)


def xmlstr(node):
    """ Helper function dumping the full XML representation of a node
    """
    return ElementTree.tostring(node, encoding="unicode", method="xml")


def innerXML(node):
    """ Helper function dumping the innerXML content of a node
    """
    return str(node.text or '') + ''.join(xmlstr(c) for c in node)


class Wrapper(Mapping):
    """ The core of the xmlasdict solution is a wrapper around etree nodes that fake some dict like look on their content
    """

    def __init__ (self, node: ElementTree.Element):
        assert isinstance(node, ElementTree.Element), f"Wrapper only designed to work with xml.etree.ElementTree.Element not '{type(node)}'"
        self._node = node

    def keys(self):
        """ returns a set of nested items (= attributes (@ prefixed) and nested unique tags)
        """
        keys = set()  # todo consider how important it is these keyse should be kept in order? if so we should use a list in stead
        for attr in self._node.attrib:
            keys.add('@' + attr)
        for child in self._node:
            keys.add(child.tag)
        return keys

    def __str__(self):
        """ returns the xml content of the current node as a string
        """
        return innerXML(self._node)

    def __bool__(self):
        """ returns true/false based on if the node has any content
        this allows direct usage of empty elements in if statements
        """
        return bool(str(self))

    def dumps(self):
        """ dumps the full xml representation of the current node as a string
        """
        return xmlstr(self._node)

    def __getitem__(self, key: str):
        log.debug(f"accessing [{key}] inside tag {self._node.tag}")
        assert key is not None and isinstance(key, str) and len(key) > 0, f"Cannot get attribute with invalid key '{key}'"
        # @ prefix indicates looking up attributes
        if key[0] == '@':
            attr_key = key[1:]
            return Wrapper._getattribute(self._node, attr_key)
        # else
        #  TODO other special ones like #text #all
        return Wrapper._getchildren(self._node, key)

    def __getattr__(self, key: str):
        log.debug(f"accessing .{key} inside tag {self._node.tag}")
        assert key is not None and len(key) > 0, f"Cannot get children with invalid key '{key}'"
        return Wrapper._getchildren(self._node, key)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    @staticmethod
    def build(node):
        assert node is not None, "cannot wrap None"
        if isinstance(node, Wrapper):  # the wrapper is already there!
            return node
        # else
        if isinstance(node, list):
            assert len(node) > 0, "cannot wrap empty node lists"
            if len(node) > 1:
                return IterWrapper(node)
            else:
                node = node[0] # unpack the single element from the list
        # else - and also if we unpacked that single element !
        return Wrapper(node)

    @staticmethod
    def _getchildren(node, key: str):
        found_elms = node.findall(key)
        if len(found_elms) == 0:
            raise AttributeError(f"Current node has no child with tag '{key}'")
        return Wrapper.build(found_elms)

    @staticmethod
    def _getattribute(node, attr_key: str):
        if attr_key not in node.attrib:
            raise AttributeError(f"Current node has no attribute with name '{attr_key}'")
        return node.attrib[attr_key]


class IterWrapper(Wrapper):
    """ Wraps a list of elements
    """
    def __init__(self, node_list):
        assert len(node_list) > 1, "Do not use IterWrapper for empty or single item lists."
        self._nodes = node_list  # original nodes
        self._wrappers = list(map(lambda n: Wrapper.build(n), node_list))  # nodes, ready wrapped


    def __str__(self):
        if len(self._nodes) == 1:
            log.debug(f"unwrap first --> {self._nodes[0]}")
            return str(self._wrappers[0])
        else:
            return str(list(map(lambda w: str(w), self._wrappers)))

    def __getitem__(self, index):
        log.debug(f"accessing [{index}] inside list[{len(self._nodes)}]")
        assert isinstance(index, (int, slice)), "IterWrapper is only subscriptable by int or slice"
        log.debug(f"my self._nodes are {self._nodes}")
        log.debug(f"my self._wrappers are {self._wrappers}")
        sublist = self._nodes[index]
        log.debug(f"sublist at [{index}] has size={len(sublist)}")
        return Wrapper.build(sublist)

    def __iter__(self):
        return iter(self._wrappers)

    def __len__(self):
        return len(self._wrappers)

    # todo consider __getitem__ to also support indices [0] and even slices [2:5]
    # see --> https://stackoverflow.com/questions/33587459/which-exception-should-getitem-setitem-use-with-an-unsupported-slice-ste


class DocumentWrapper(Wrapper):
    pass


class ElementWrapper(Wrapper):
    pass


class AttributeWrapper(Wrapper):
    pass


class CommentsWrapper(Wrapper):
    pass
