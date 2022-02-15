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

    def __init__(self, node: ElementTree.Element):
        assert isinstance(node, ElementTree.Element), f"Wrapper only works with xml.etree.ElementTree.Element not '{type(node)}'"
        self._node = node

    def keys(self):
        """ returns a set of nested items (= attributes (@ prefixed) and nested unique tags)
        """
        return set() | self._attr_keys() | self._elm_keys()  # the union of attr_keys and elm_keys

    def _attr_keys(self):
        """ the set of available attribute names presented as __getitem__() keys
        """
        keys = set()
        for attr in self._node.attrib:
            keys.add('@' + attr)
        return keys

    def _elm_keys(self):
        """ the set of nested element_tags presented as __getitem__() keys
        """
        keys = set()
        for child in self._node:
            keys.add(child.tag)
        return keys

    def __str__(self):
        """ returns the xml content of the current node as a string
        """
        return innerXML(self._node).strip()

    def __bool__(self):
        """ returns true/false based on if the node has any content
        this allows direct usage of empty elements in if statements
        """
        return bool(str(self))

    def dumps(self):
        """ dumps the full xml representation of the current node as a string
        """
        return xmlstr(self._node)

    @property
    def tag(self):
        return self._node.tag

    def unpack(self):
        """ retrieves highest level row content down from a chain of (unuseful) single wrapper_nodes
        """
        log.debug(f"unpack at {self._node.tag}")
        nested_tags = self._elm_keys()
        if len(nested_tags) > 1 or len(nested_tags) == 0:   # if there are (or) mixed elements under this node (or) none
            return IterWrapper([self])                      # then unpack ends here
        # else actually (try) unpack if all nested elements are of the same flavour
        content = Wrapper._getchildren(self._node, '*')
        return content.unpack()

    def unwrap(self):
        """ turns the content into a native py representation (dict for Wrapper and list for IterWrapper)
        """
        # handle both nested element as well as str (attribute) returns
        def unwrap(value): return value.unwrap() if isinstance(value, Wrapper) else value
        return {k: unwrap(self[k]) for k in set(self)} if len(set(self)) > 0 else str(self)

    def __getitem__(self, key: str):
        log.debug(f"accessing [{key}] inside tag {self._node.tag}")
        assert key is not None and isinstance(key, str) and len(key) > 0, f"Cannot get attribute with invalid key '{key}'"
        # @ prefix indicates looking up attributes
        if key[0] == '@':
            attr_key = key[1:]
            return Wrapper._getattribute(self._node, attr_key)
        # else
        # TODO maybe consider other special ones like #text to grab the equivalent of xpath text() ??
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
                node = node[0]  # unpack the single element from the list
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
        assert len(node_list) > 0, "Do not use IterWrapper for empty lists."
        self._nodes = node_list  # original nodes
        self._wrappers = list(map(lambda n: Wrapper.build(n), node_list))  # nodes, ready wrapped

    def __str__(self):
        if len(self._nodes) == 1:
            return str(self._wrappers[0])
        else:
            return str(list(map(lambda w: str(w), self._wrappers)))

    def __getitem__(self, index):
        log.debug(f"accessing [{index}] inside list[{len(self._nodes)}]")
        assert isinstance(index, (int, slice)), "IterWrapper is only subscriptable by int or slice"
        sublist = self._nodes[index]
        return Wrapper.build(sublist)

    def __iter__(self):
        return iter(self._wrappers)

    def __len__(self):
        return len(self._wrappers)

    def unpack(self):
        return self  # the goal of unpack is to end when we are at the level if iterables

    def unwrap(self):
        """ turns the content into a native py representation (dict for Wrapper and list for IterWrapper)
        """
        return [w.unwrap() for w in self._wrappers]

    def dumps(self):
        return ''.join([w.dumps() for w in self._wrappers])

    @property
    def tag(self):
        return [n.tag for n in self._wrappers]
