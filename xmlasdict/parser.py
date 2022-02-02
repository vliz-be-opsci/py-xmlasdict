import os
from xml.etree import ElementTree
from .wrapper import Wrapper


def parse(input: str):
    """ Parses the xml into a xmlasdict structure that allows approaching the wrapped emltree as a (somewhat) regular dict
    """
    xml = None
    if os.path.isfile(input):
        xml = ElementTree.parse(input)
    elif isinstance(input, str): # overdone to enforce and input[0] == '<' and input[-1] == '>':
        xml = ElementTree.fromstring(input) # TODO check if we should not apply .getroot() on this 

    assert xml is not None, f"could not parse input {input}"
    return Wrapper.build(xml)
