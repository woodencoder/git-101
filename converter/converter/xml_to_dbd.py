import xml.dom.minidom as md
from components import (xml_converter, dbd_builder)


def parse(xdb, dbd):
    # parsing an xml file
    tasks = md.parse(xdb)

    # converting xml to ram
    schema = xml_converter.XML_Converter(tasks).xml_to_ram()

    # converting ram to dbd
    builder = dbd_builder.DBD_Builder(schema=schema)
    builder.ram_to_dbd(dbd)