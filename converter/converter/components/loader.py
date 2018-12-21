from models import Schema, Domain, Table, Constraint, Field, Index, Item
import sqlite3
import uuid
import data.dbd_const as script


class Loader:
    def __init__(self, file_path):
        self.file_path = file_path

    def dbd_to_ram(self, db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        schema = Schema()
        db_schema = cur.execute("SELECT * from dbd$schemas").fetchall()
        for item in db_schema:
            schema.name = item[1]
            schema.description = item[2]
            schema.domains = self._getDbDomains(cur)
            schema.tables = self._getDbTables(cur, item[0])

        conn.commit()
        conn.close()

        return schema

    def _getDbDomains(self, cur):
        domains = []

        db_domains = cur.execute("SELECT * from dbd$domains").fetchall()
        for domain in db_domains:
            tmp = Domain()

            if domain[1] is not None:
                tmp.name = str(domain[1])
            if domain[2] is not None:
                tmp.description = str(domain[2])
            if domain[3] is not None:
                tmp.type = self._getDbDataType(cur, domain[3])
            if domain[4] is not None:
                tmp.length = str(domain[4])
            if domain[5] is not None:
                tmp.char_length = str(domain[5])
            if domain[6] is not None:
                tmp.precision = str(domain[6])
            if domain[7] is not None:
                tmp.scale = str(domain[7])
            if domain[8] is not None:
                tmp.width = str(domain[8])
            if domain[9] is not None:
                tmp.align = str(domain[9])
            # props
            tmp.show_null = domain[10]
            tmp.show_lead_nulls = domain[11]
            tmp.thousands_separator = domain[12]
            tmp.summable = domain[13]
            tmp.case_sensitive = domain[14]

            domains.append(tmp)
        return domains

    def _getDbTables(self, cur, schema_id):
        tables = []

        db_tables = cur.execute(""" SELECT * from dbd$tables
                                    WHERE schema_id = :id
                                    GROUP BY id""",
                                {"id": schema_id}).fetchall()

        for table in db_tables:
            tmp = Table()

            if table[2] is not None:
                tmp.name = str(table[2])
            if table[3] is not None:
                tmp.description = str(table[3])

            tmp.add = table[4]
            tmp.edit = table[5]
            tmp.delete = table[6]

            if table[7] is not None:
                tmp.access_level = str(table[7])
            if table[8] is not None:
                tmp.ht_table_flags = str(table[8])
            tmp.fields = self._getDbFields(cur, table[0])
            tmp.constraints = self._getDbConstraints(cur, table[0])
            tmp.indices = self._getDbIndices(cur, table[0])

            tables.append(tmp)

        return tables

    def _getDbFields(self, cur, table_id):
        fields = []

        db_fields = cur.execute(""" SELECT * from dbd$fields
                                    WHERE table_id = :id""",
                                {"id": table_id}).fetchall()

        for field in db_fields:
            tmp = Field()

            if field[3] is not None:
                tmp.name = str(field[3])
            if field[4] is not None:
                tmp.rname = str(field[4])
            if field[5] is not None:
                tmp.description = str(field[5])
            if field[6] is not None:
                tmp.domain = self._getDbDomainName(cur, field[6])
            tmp.input = field[7]
            tmp.edit = field[8]
            tmp.show_in_grid = field[9]
            tmp.show_in_details = field[10]
            tmp.is_mean = field[11]
            tmp.autocalculated = field[12]
            tmp.required = field[13]

            fields.append(tmp)

        return fields

    def _getDbConstraints(self, cur, table_id):
        constraints = []

        db_constraints = cur.execute(""" SELECT * from dbd$constraints
                                    WHERE table_id = :id""",
                                     {"id": table_id}).fetchall()

        for constraint in db_constraints:
            tmp = Constraint()

            if constraint[2] is not None:
                tmp.name = str(constraint[2])
            if constraint[3] is not None:
                tmp.kind = str(constraint[3])
            if constraint[4] is not None:
                tmp.reference = self._getDbTableName(cur, constraint[4])
            if constraint[5] is not None:
                tmp.reference_type = str(constraint[5])
            tmp.has_value_edit = constraint[6]
            tmp.cascading_delete = constraint[7]
            tmp.expression = constraint[8]
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
                tmp.name = str(index[2])
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
