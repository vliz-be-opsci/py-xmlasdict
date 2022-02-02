import xml.etree.ElementTree as ET
from .wrapper import Wrapper



def parse(input: str):
    #handle variants: file, string snippet, ...
    #if input == file path and file exists
    xml = ET.parse(input)
    # else if input starts with < and ends with >
    # xml = ET.from_string(input)

    return Wrapper.build(xml)
