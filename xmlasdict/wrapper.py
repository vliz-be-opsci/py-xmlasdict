# Use this file to describe the datamodel handled by this module
# we recommend using abstract classes to achieve proper service and interface insulation
from abc import ABC, abstractmethod


class Wrapper(ABC):
    """ The core of the xmlasdict solution is a wrapper around etree nodes that fake some dict like look on their content
    """
    # TODO declare some abstract methods that are available at all levels
    #  those will probably be the methods that introduce the dict-like behaviour (so __iter__ __next__ and __getattribute__ so maybe weird to declare thos abstract?

    @staticmethod
    def build(node_to_wrap):
        # todo decide based on type of node which one to build
        pass



class DocumentWrapper(Wrapper):
    pass

    
class ElementWrapper(Wrapper):
    pass


class AttributeWrapper(Wrapper):
    pass


class CommentsWrapper(Wrapper):
    pass
