from models import Schema, Domain, Table, Constraint, Field, Index, Item
import sqlite3
import uuid
import data.dbd_const as script


class Loader:
    def __init__(self, file_path):
        self.file_path = file_path

    def dbd_to_ram(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()

        db_schema = cur.execute("SELECT * from dbd$schemas").fetchall()
        schema_metadata = self._getMetadata(cur, "dbd$schemas")

        for item in db_schema:
            schema_dictionary = dict(zip(schema_metadata, list(item)))
            schema = Schema(schema_dictionary)
            schema.domains = self._getDbDomains(cur)

            if schema_dictionary.get("id") is not None:
                schema.tables = self._getDbTables(cur, schema_dictionary["id"])

        conn.commit()
        conn.close()

        return schema

    def _getDbDomains(self, cur):
        domains = []

        db_domains = cur.execute("SELECT * from dbd$domains").fetchall()
        domain_metadata = self._getMetadata(cur, "dbd$domains")

        for domain in db_domains:
            domain_dictionary = dict(zip(domain_metadata, list(domain)))
            tmp = Domain(domain_dictionary)
            data_type = cur.execute("SELECT * FROM dbd$data_types WHERE id = :type_id", {"type_id": tmp.data_type_id}).fetchall()
            tmp.type = data_type[0][1]
            domains.append(tmp)

        return domains

    def _getDbTables(self, cur, schema_id):
        tables = []

        db_tables = cur.execute(""" SELECT * from dbd$tables
                                    WHERE schema_id = :id
                                    GROUP BY id""",
                                {"id": schema_id}).fetchall()
        tables_metadata = self._getMetadata(cur, "dbd$tables")

        for table in db_tables:
            table_dictionary = dict(zip(tables_metadata, list(table)))
            tmp = Table(table_dictionary)

            if table_dictionary.get("id") is not None:
                tmp.fields = self._getDbFields(cur, table_dictionary["id"])
                tmp.constraints = self._getDbConstraints(cur, table_dictionary["id"])
                tmp.indices = self._getDbIndices(cur, table_dictionary["id"])

            tables.append(tmp)

        return tables

    def _getDbFields(self, cur, table_id):
        fields = []

        db_fields = cur.execute(""" SELECT * from dbd$fields
                                    WHERE table_id = :id""",
                                {"id": table_id}).fetchall()
        field_metadata = self._getMetadata(cur, "dbd$fields")
        for field in db_fields:
            field_dictionary = dict(zip(field_metadata, list(field)))
            tmp = Field(field_dictionary)

            if field_dictionary["domain_id"] is not None:
                tmp.domain = self._getDbDomainName(cur, domain_id=field_dictionary["domain_id"])

            fields.append(tmp)

        return fields

    def _getDbConstraints(self, cur, table_id):
        constraints = []

        db_constraints = cur.execute(""" SELECT * from dbd$constraints
                                    WHERE table_id = :id""",
                                     {"id": table_id}).fetchall()
        field_metadata = self._getMetadata(cur, "dbd$constraints")
        for constraint in db_constraints:
            constraints_dictionary = dict(zip(field_metadata, list(constraint)))
            tmp = Constraint(constraints_dictionary)



            if constraints_dictionary["id"] is not None:
                tmp.items = self._getDbConstraintDetails(cur, constraint[0])

            constraints.append(tmp)

        return constraints

    def _getDbConstraintDetails(self, cur, constraint_id):
        items = []

        db_details = cur.execute("""SELECT * from dbd$constraint_details
                                  WHERE constraint_id = :id""",
                                 {"id": constraint_id}).fetchall()

        for item in db_details:
            items.append(self._getDbFieldName(cur, item[3]))

        return items

    def _getDbIndices(self, cur, table_id):
        indices = []

        db_indices = cur.execute(""" SELECT * from dbd$indices
                                    WHERE table_id = :id""",
                                 {"id": table_id}).fetchall()

        for index in db_indices:
            tmp = Index()

            for item in self._getDbIndexDetails(cur, index[0]):
                tmp.fields.append(item.name)

            if index[2] is not None:
                tmp.name = str(index[2].encode('utf-8'))
            tmp.fulltext = index[3]
            if index[4] != "simple":
                tmp.uniqueness = index[4]

            indices.append(tmp)

        return indices

    def _getDbIndexDetails(self, cur, index_id):
        items = []

        db_details = cur.execute("""SELECT * from dbd$index_details
                                WHERE index_id = :id""",
                                 {"id": index_id}).fetchall()

        for item in db_details:
            tmp = Item()
            tmp.name = self._getDbFieldName(cur, item[3])
            tmp.expression = item[4]
            tmp.desc = item[5]

            items.append(tmp)

        return items

    def _getDbDataType(self, cur, type_id):
        return cur.execute("""  SELECT type_id from dbd$data_types
                                WHERE id =:id""", {"id": type_id}).fetchone()[0]

    def _getDbDomainName(self, cur, domain_id):
        return cur.execute("""SELECT name from dbd$domains
                            WHERE id = :id""",
                           {"id": domain_id}).fetchone()[0]

    def _getDbFieldName(self, cur, field_id):
        return cur.execute("""SELECT name from dbd$fields
                            WHERE id = :id""",
                           {"id": field_id}).fetchone()[0]

    def _getDbTableName(self, cur, table_id):
        return cur.execute("""SELECT name from dbd$tables
                            WHERE id = :id""",
                           {"id": table_id}).fetchone()[0]

    def _getMetadata(self, cur, table_name):
        cur.execute('PRAGMA TABLE_INFO({})'.format(table_name))

        # collect names in a list
        metadata = [tup[1] for tup in cur.fetchall()]
        return metadata