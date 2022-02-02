import os
import xml.etree.ElementTree as ET
from .wrapper import Wrapper


def parse(input: str):
    """ Parses the xml into a xmlasdict structure that allows approaching the wrapped emltree as a (somewhat) regular dict
    """
    xml = None
    if os.path.isfile(input):
        xml = ET.parse(input)
    elif isinstance(input, str): # overdone to enforce and input[0] == '<' and input[-1] == '>':
        xml = ET.fromstring(input)

    assert xml is not None, f"could not parse input {input}"
    return Wrapper.build(xml)
