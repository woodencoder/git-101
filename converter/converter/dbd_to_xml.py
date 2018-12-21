from components import (loader, xml_builder)


def parse(dbd, xdb):
    # converting dbd to ram
    schema1 = loader.Loader(dbd).dbd_to_ram()

    # converting ram to xml
    result = xml_builder.XML_builder(schema=schema1).ram_to_xml()

    with open(xdb, "w") as created_file:
        created_file.write(result.toprettyxml(encoding="utf-8").decode("utf-8"))