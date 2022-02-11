import os
from xml.etree import ElementTree
from .wrapper import Wrapper


def parse(input: str):
    """ Parses the xml into a xmlasdict structure that allows approaching the wrapped emltree as a (somewhat) regular dict
    """
    xml = None
    if os.path.isfile(input):
        xml = ElementTree.parse(input).getroot()
    elif isinstance(input, str):
        xml = ElementTree.fromstring(input)

    assert xml is not None, f"could not parse input {input}"
    return Wrapper.build(xml)
