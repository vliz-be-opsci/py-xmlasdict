# Use this file to describe the datamodel handled by this module
# we recommend using abstract classes to achieve proper service and interface insulation
from abc import ABC, abstractmethod
from xml.etree import ElementTree
import logging


log = logging.getLogger(__name__)


class Wrapper(ABC):
    """ The core of the xmlasdict solution is a wrapper around etree nodes that fake some dict like look on their content
    """
    # TODO declare some abstract methods that are available at all levels
    #  those will probably be the methods that
    #    - introduce the dict-like behaviour
    #      (so __iter__ __next__ and __getattribute__ so maybe weird to declare thos abstract?
    #    - handle proper serialisation
    #      ( so some __str__ call to ElementTree.tostring(node))

    def __init__ (self, node):
        self._node = node

    def __str__(self):
        xmlstr = ElementTree.tostring(self._node, encoding='unicode', method='xml')
        return xmlstr


    @staticmethod
    def build(node):
        log.debug(f"building wrapper for {node}")
        # todo decide based on type of node which one to build
        # for now simply return the base class
        return Wrapper(node)



class DocumentWrapper(Wrapper):
    pass


class ElementWrapper(Wrapper):
    pass


class AttributeWrapper(Wrapper):
    pass


class CommentsWrapper(Wrapper):
    pass
