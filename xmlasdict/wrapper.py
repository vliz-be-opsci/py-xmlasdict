# Use this file to describe the datamodel handled by this module
# we recommend using abstract classes to achieve proper service and interface insulation
from abc import ABC, abstractmethod
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


class Wrapper(ABC):
    """ The core of the xmlasdict solution is a wrapper around etree nodes that fake some dict like look on their content
    """

    def __init__ (self, node):
        self._node = node

    def __str__(self):
        return innerXML(self._node)

    def dumps(self):
        return xmlstr(self._node)

    def __getitem__(self, key: str):
        assert key is not None and len(key) > 0, f"Cannot get attribute with invalid key '{key}'"
        # @ prefix indicates looking up attributes
        if key[0] == '@':
            attr_key = key[1:]
            return self._node.attrib[attr_key]
        raise ValueError(f"key '{key}' not supported")

    def __getattr__(self, key: str):
        assert key is not None and len(key) > 0, f"Cannot get attribute with invalid key '{key}'"
        # todo
        # find the 'key' child-elements inside the node and return an iterator of wrapped children
        log.debug(f"accessing {key} inside tag {self._node.tag}")
        found_elms = list(self._node.iter(key))
        if len(found_elms) == 0:
            raise AttributeError(f"Current node has no attribute or child for key '{key}'")
        if len(found_elms) == 1:
            return Wrapper(found_elms[0])
        # else
        return IterWrapper(found_elms)

    @staticmethod
    def build(node):
        log.debug(f"building wrapper for {node}")
        # todo decide based on type of node which one to build
        # for now simply return the base class
        return Wrapper(node)


class IterWrapper(Wrapper):
    """ Wraps a list of elements
    """
    def __init__(self, node_list):
        assert len(node_list) > 1, "Do not use IterWrapper for empty or single item lists."
        self._nodes = list(map(lambda n: Wrapper.build(n), node_list))

    def __str__(self):
        if len(self._nodes) == 1:
            log.debug(f"unwrap first --> {self._nodes[0]}")
            return str(self._nodes[0])
        else:
            return str(list(map(lambda n: str(n), self._nodes)))

    def __iter__(self):
        return iter(self._nodes)

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
