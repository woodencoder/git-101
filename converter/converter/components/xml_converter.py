from models import Schema, Domain, Table, Constraint, Field, Index, Item

class XML_Converter:
    def __init__(self, xml):
        self.xml = xml

    def xml_to_ram(self):
        schema = Schema()
        for attributeName, attributeValue in self.xml.documentElement.attributes.items():
            if attributeName.lower() == "fulltext_engine":
                schema.fulltext_engine = attributeValue
            elif attributeName.lower() == "version":
                schema.version = attributeValue
            elif attributeName.lower() == "name":
                schema.name = attributeValue
            elif attributeName.lower() == "description":
                schema.description = attributeValue
            else:
                raise ValueError("Incorrect attribute name \"{}\" in tag \"{}\"".format(attributeName, schema.nodeName))

            schema.domains = self._getDomains()
            schema.tables = self._getTables(self.xml)

        return schema

    def _getDomains(self):
        domains = []
        for domain in self.xml.getElementsByTagName("domain"):
            tmp = Domain()

            for attributeName, attributeValue in domain.attributes.items():
                if attributeName.lower() == "name":
                    tmp.name = attributeValue
                elif attributeName.lower() == "description":
                    tmp.description = attributeValue
                elif attributeName.lower() == "type":
                    tmp.type = attributeValue
                elif attributeName.lower() == "align":
                    tmp.align = attributeValue
                elif attributeName.lower() == "width":
                    tmp.width = attributeValue
                elif attributeName.lower() == "precision":
                    tmp.precision = attributeValue
                elif attributeName.lower() == "props":
                    for prop in attributeValue.split(", "):
                        if prop == "show_null":
                            tmp.show_null = True
                        elif prop == "summable":
                            tmp.summable = True
                        elif prop == "case_sensitive":
                            tmp.case_sensitive = True
                        elif prop == "show_lead_nulls":
                            tmp.show_lead_nulls = True
                        elif prop == "thousands_separator":
                            tmp.thousands_separator = True
                        else:
                            raise ValueError("Invalid format of props string: {}".format(attributeValue))
                elif attributeName.lower() == "char_length":
                    tmp.char_length = attributeValue
                elif attributeName.lower() == "length":
                    tmp.length = attributeValue
                elif attributeName.lower() == "scale":
                    tmp.scale = attributeValue
                else:
                    raise ValueError(
                        "Incorrect attribute name \"{}\" in tag \"{}\" ".format(attributeName, domain.nodeName))

            domains.append(tmp)
        return domains

    def _getTables(self, xml):
        tables = []
        for table in xml.getElementsByTagName("table"):
            tmp = Table()
            for attributeName, attributeValue in table.attributes.items():
                if attributeName.lower() == "name":
                    tmp.name = attributeValue
                elif attributeName.lower() == "description":
                    tmp.description = attributeValue
                elif attributeName.lower() == "props":
                    for prop in attributeValue.split(", "):
                        if prop == "add":
                            tmp.add = True
                        elif prop == "edit":
                            tmp.edit = True
                        elif prop == "delete":
                            tmp.delete = True
                        else:
                            raise ValueError("Invalid format of props string: {}".format(attributeValue))
                elif attributeName.lower() == "ht_table_flags":
                    tmp.ht_table_flags = attributeValue
                elif attributeName.lower() == "access_level":
                    tmp.access_level = attributeValue
                else:
                    raise ValueError(
                        "Incorrect attribute name \"{}\" in tag \"{}\" ".format(attributeName, table.nodeName))

            tmp.fields = self._getFields(table)
            tmp.constraints = self._getConstraints(table)
            tmp.indices = self._getIndices(table)
            tables.append(tmp)
        return tables

    def _getFields(self, xml):
        if xml.nodeName != "table":
            raise ValueError("Is not a table")

        fields = []
        for field in xml.getElementsByTagName("field"):
            tmp = Field()
            for attributeName, attributeValue in field.attributes.items():
                if attributeName.lower() == "name":
                    tmp.name = attributeValue
                elif attributeName.lower() == "rname":
                    tmp.rname = attributeValue
                elif attributeName.lower() == "domain":
                    tmp.domain = attributeValue
                elif attributeName.lower() == "description":
                    tmp.description = attributeValue
                elif attributeName.lower() == "props":
                    for prop in attributeValue.split(", "):
                        if prop == "input":
                            tmp.input = True
                        elif prop == "edit":
                            tmp.edit = True
                        elif prop == "show_in_grid":
                            tmp.show_in_grid = True
                        elif prop == "show_in_details":
                            tmp.show_in_details = True
                        elif prop == "is_mean":
                            tmp.is_mean = True
                        elif prop == "autocalculated":
                            tmp.autocalculated = True
                        elif prop == "required":
                            tmp.required = True
                        else:
                            raise ValueError("Invalid format of props string: {}".format(attributeValue))
                else:
                    raise ValueError(
                        "Incorrect attribute name \"{}\" in tag \"{}\" ".format(attributeName, field.nodeName))

            fields.append(tmp)
        return fields

    def _getConstraints(self, xml):
        if xml.nodeName != "table":
            raise ValueError("Is not a table")

        constraints = []
        for constraint in xml.getElementsByTagName("constraint"):
            tmp = Constraint()
            for attributeName, attributeValue in constraint.attributes.items():
                if attributeName.lower() == "name":
                    tmp.name = attributeValue
                elif attributeName.lower() == "kind":
                    tmp.kind = attributeValue
                elif attributeName.lower() == "items":
                    tmp.items = [attributeValue]
                elif attributeName.lower() == "props":
                    for prop in attributeValue.split(", "):
                        if prop == "has_value_edit":
                            tmp.has_value_edit = True
                        elif prop == "cascading_delete":
                            tmp.cascading_delete = True
                        elif prop == "full_cascading_delete":
                            tmp.full_cascading_delete = True
                        else:
                            raise ValueError("Invalid format of props string: {}".format(attributeValue))
                elif attributeName.lower() == "reference":
                    tmp.reference = attributeValue
                else:
                    raise ValueError(
                        "Incorrect attribute name \"{}\" in tag \"{}\" ".format(attributeName, attributeValue))

            constraints.append(tmp)
        return constraints

    def _getIndices(self, xml):
        if xml.nodeName != "table":
            raise ValueError("Is not a table")

        indexes = []
        for index in xml.getElementsByTagName("index"):
            tmp = Index()
            if index.hasChildNodes():
                for item in index.getElementsByTagName("item"):
                    pass
            else:
                item = Item()
                item.name = index.getAttribute("field")
                tmp.fields.append(item.name)
            for attributeName, attributeValue in index.attributes.items():
                if attributeName.lower() == "field":
                    pass
                elif attributeName.lower() == "props":
                    for prop in attributeValue.split(", "):
                        if prop == "fulltext":
                            tmp.fulltext = True
                        elif prop == "uniqueness":
                            tmp.uniqueness = True
                        else:
                            raise ValueError("Invalid format of props string: {}".format(attributeValue))
                else:
                    raise ValueError(
                        "Incorrect attribute name \"{}\" in tag \"{}\" ".format(attributeName, index.nodeName))
            indexes.append(tmp)
        return indexes
