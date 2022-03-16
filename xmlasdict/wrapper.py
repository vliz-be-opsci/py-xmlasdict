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
    """ The core of the xmlasdict solution is a wrapper around etree nodes that fake some dict like look on their content.
    This is the basic return-type of the function :func:`~xmlasdict.parse`.
    Do not instantiate this objects yourself,
    instead use :func:`~xmlasdict.parse` or (if you must) the static :func:`~Wrapper.build`.

    The dict-like behaviour of this object reflects the fact that one can use wrapper[key] notation to navigate the XML tree.
    At each stage in that traversal a similar :class:`~Wrapper` will be returned allowing further navigation.
    Repeated child-elements with the same tag-name will be returned (in order) as list-like objects using the :class:`~IterWrapper`.

    Additionally, like a dict one can naturally iterate its keys in a "for k in wrapper:"-loop.
    The set of these can also be explicitly requested through :func:`~Wrapper.keys`.

    Note that this set of keys will also list the associated attributes through the xpath-like ``'@attribute_name'`` notation.
    Naturally this means that these can be used in the ``wrapper['@attribute_name']`` notation to retrieve their string content.

    While behaving like a dict, the :class:`~Wrapper` also supports some standard type conversions:

    - str(wrapper) will produce the (inner) XML content of the current node. (respecting whitespace and mixed-content)
    - bool(wrapper) will produce False if the XML element at this level is <empty />

    Beyond the expected dict[key] access these :class:`Wrapper` objects also allow for path-like accessor-calls.
    e.g. wrapper['.//x'] will not only return the direct children, but (depth-first or xml-document-order) all descendants.
    The allowed syntax for these paths follow the ElementTree.node.findall support.
    """

    def __init__(self, node: ElementTree.Element):
        assert isinstance(node, ElementTree.Element), f"Wrapper only works with xml.etree.ElementTree.Element not '{type(node)}'"
        self._node = node

    def keys(self):
        """ Returns a set of nested items (= attributes (@ prefixed) and nested unique tags).
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
        """ Dumps the full xml representation of the current node as a string.
        wrapper.dumps() is distinct to str(wrapper) in that will include the wrapping tag
        (i.e. the outerXML) rather than only the nested content (innerXML).
        """
        return xmlstr(self._node)

    @property
    def tag(self):
        """ Returns the tag-name of the current level in the XML tree.
        """
        return self._node.tag

    def unpack(self, tag: str = None):
        """ Retrieves the highest-level row content down from a chain of (un-useful) single wrapper_nodes.
        This is a convenience method allowing one to easily descend down into any single-wrapping tags
        down to the actual repeated content.

        :param tag: stop unwrapping if the tag-name matches
        """
        nested_tags = self._elm_keys()  # remeber this is a set of (unique) child elm keys
        mytag = self._node.tag

        log.debug(f"unpacking {mytag} to {nested_tags} and stopping at {tag}")

        # if there are (or) mixed elements under this node (or) none (or) the tag-name matches the requested param tag
        if len(nested_tags) > 1 or len(nested_tags) == 0 or tag == mytag:
            return IterWrapper([self])                      # then unpack ends here
        # else actually (try) unpack if all nested elements are of the same flavour
        content = Wrapper._getchildren(self._node, '*')
        return content.unpack(tag=tag)

    def unwrap(self):
        """ Turns the content into a native py representation (dict).
        """
        # handle both nested element as well as str (attribute) returns
        def unwrap(value): return value.unwrap() if isinstance(value, Wrapper) else value
        return {k: unwrap(self[k]) for k in set(self)} if len(set(self)) > 0 else str(self)

    def copy(self):
        """ Turns the content into a native py representation (dict for :class:`~Wrapper` and list for :class:`IterWrapper`)
        """
        return self.unwrap()

    def __getitem__(self, key: str):
        log.debug(f"accessing [{key}] inside tag {self._node.tag}")
        assert key is not None and isinstance(key, str) and len(key) > 0, f"Cannot get attribute with invalid key '{key}'"
        force_list = False
        # @ prefix indicates looking up attributes
        if key[0] == '@':
            attr_key = key[1:]
            return Wrapper._getattribute(self._node, attr_key)
        # else

        # the [] suffix indicates we want a forced list return
        if key[-2:] == '[]':
            key = key[:-2]  # truncate the key
            force_list = True
        # TODO maybe consider other special ones like #text to grab the equivalent of xpath text() ??
        return Wrapper._getchildren(self._node, key, force_list)

    def __getattr__(self, key: str):
        log.debug(f"accessing .{key} inside tag {self._node.tag}")
        assert key is not None and len(key) > 0, f"Cannot get children with invalid key '{key}'"
        return Wrapper._getchildren(self._node, key)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    @staticmethod
    def build(node, force_list: bool = False):
        """ Actually "builds" a :class:`~Wrapper` or :class:`~IterWrapper` by introspecting the passed node
        Normally one avoids using this to build your own wrappers in favour of just using the :func:`~xmlasdict.parse` method.

        :param node: can be a :class:`~Wrapper` that doesn't need further wrapping or an ElementTree.node or a list of those
        :param force_list: enforce returning a list of nodes (i.e an :class:`~IterWrapper`)
        """
        assert node is not None, "cannot wrap None"
        if isinstance(node, Wrapper):  # the wrapper is already there!
            return node if not force_list else IterWrapper([node])
        # else
        if isinstance(node, list):
            assert len(node) > 0 or force_list, "cannot wrap empty node lists unless force_list == True"
            if len(node) > 1 or force_list is True:
                return IterWrapper(node) if len(node) > 0 else []
            else:
                node = node[0]  # unpack the single element from the list
        # else - and also if we unpacked that single element !
        return Wrapper(node)

    @staticmethod
    def _getchildren(node, key: str, force_list: bool = False):
        found_elms = node.findall(key)
        if len(found_elms) == 0 and not force_list:  # enforce-list mode prefers an empty list over an error
            raise AttributeError(f"Current node has no child with tag '{key}'")
        return Wrapper.build(found_elms, force_list)

    @staticmethod
    def _getattribute(node, attr_key: str):
        if attr_key not in node.attrib:
            raise AttributeError(f"Current node has no attribute with name '{attr_key}'")
        return node.attrib[attr_key]


class IterWrapper(Wrapper):
    """ Wraps a list of elements; and as such does smart things to make the whole navigating experience as py-natural as possible.
    So, some clever 'list-like' behaviour is added onto what the base :class:`Wrapper` -class already provides.

    As a list-like beast this representation of the nested XML content is not subscriptable by str
    (name of child-element or ``@attribute``) but instead by int or slice.
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

    def unpack(self, tag: str = None):
        """ Returns self, as by nature the IterWrapper is the level not to be further unpacked.
        """
        return self  # the goal of unpack is to end when we are at the level if iterables

    def unwrap(self):
        """ Turns the content into a native py representation (list).
        """
        return [w.unwrap() for w in self._wrappers]

    def dumps(self):
        """ Returns the joined outerXML of the various contained wrappers.
        """
        return ''.join([w.dumps() for w in self._wrappers])

    @property
    def tag(self):
        """ Returns the list of tags of the contained wrappers.
        """
        return [n.tag for n in self._wrappers]
