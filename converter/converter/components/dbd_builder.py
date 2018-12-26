import sqlite3
import uuid
import data.dbd_const as script

class DBD_Builder:

    def __init__(self, schema):
        self.schema = schema

    def ram_to_dbd(self, db_path):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()

            cur.executescript(script.SQL_DBD_Init)
            cur.execute("INSERT into dbd$schemas(name) values (?)", (self.schema.name,))
            if (self.schema.description is not None):
                cur.execute("UPDATE dbd$schemas SET description = :desc WHERE name=:name",
                            {"desc": self.schema.description, "name": self.schema.name})

            for domain in self.schema.domains:
                cur.execute("INSERT into dbd$domains(name, data_type_id, uuid) values (?,?,?)",
                            (domain.name, -1, str(uuid.uuid4())))
                cur.execute("""UPDATE dbd$domains SET
                                 description = :desc,
                                 length = :length,
                                 char_length = :charl,
                                 precision = :prec,
                                 scale = :scale,
                                 width = :width,
                                 align = :align,
                                 show_null = :show_null,
                                 show_lead_nulls = :show_lnulls,
                                 thousands_separator = :th_sep,
                                 summable = :summ,
                                 case_sensitive = :c_sens
                                 WHERE name=:name""",
                            {"desc": domain.description,
                             "name": domain.name,
                             "length": domain.length,
                             "charl": domain.char_length,
                             "prec": domain.precision,
                             "scale": domain.scale,
                             "width": domain.width,
                             "align": domain.align,
                             "show_null": domain.show_null,
                             "show_lnulls": domain.show_lead_nulls,
                             "th_sep": domain.thousands_separator,
                             "summ": domain.summable,
                             "c_sens": domain.case_sensitive})

                cur.execute(""" UPDATE dbd$domains
                                SET data_type_id = (
                                SELECT id from dbd$data_types WHERE dbd$data_types.type_id = :type_n) 
                                WHERE data_type_id = -1""",
                            {"type_n": domain.type})

            for table in self.schema.tables:

                cur.execute("INSERT into dbd$tables(name, uuid) values (?,?)",
                            (table.name, str(uuid.uuid4())))

                cur.execute("""UPDATE dbd$tables SET
                                        description = :desc,
                                        can_add = :can_add,
                                        can_edit = :can_edit,
                                        can_delete = :can_delete,
                                        temporal_mode = :access,
                                        means = :ht
                                        WHERE name=:name""",
                            {"desc": table.description,
                             "can_add": table.add,
                             "can_edit": table.edit,
                             "can_delete": table.delete,
                             "access": table.access_level,
                             "ht": table.ht_table_flags,
                             "name": table.name})

                cur.execute(""" UPDATE dbd$tables 
                                SET schema_id =(
                                SELECT id from dbd$schemas as sch
                                        WHERE sch.name = :name_s)""",
                            {"name_s": self.schema.name})

                table_id = cur.execute("""SELECT id from dbd$tables
                                                            WHERE dbd$tables.name = :t_name""",
                                       {"t_name": table.name}).fetchone()
                domain_ids = self.get_id(cur, """SELECT id,name FROM dbd$domains""")
                pos_f = 1

                for field in table.fields:
                    cur.execute(
                        "INSERT into dbd$fields(name, russian_short_name, table_id, position, domain_id, uuid) values (?,?,?,?,?,?)",
                        (field.name, field.rname, table_id[0], pos_f, domain_ids[domain.name], str(uuid.uuid4())))
                    pos_f += 1

                    cur.execute(""" UPDATE dbd$fields SET
                                            description = :desc,
                                            can_input = :can_i,
                                            can_edit = :can_e,
                                            show_in_grid = :show_grid,
                                            show_in_details = :show_det,
                                            is_mean = :is_mean,
                                            autocalculated = :autocalc,
                                            required = :req
                                            WHERE name = :name""",
                                {"desc": field.description,
                                 "can_i": field.input,
                                 "can_e": field.edit,
                                 "show_grid": field.show_in_grid,
                                 "show_det": field.show_in_details,
                                 "is_mean": field.is_mean,
                                 "autocalc": field.autocalculated,
                                 "req": field.required,
                                 "name": field.name})
                pos_i = 1

                for index in table.indices:

                    if index.name != None:
                        i_name = index.name
                    else:
                        i_name = '1'
                    if index.uniqueness:
                        uni = "unique"
                    else:
                        uni = "simple"
                    cur.execute(""" INSERT INTO dbd$indices(
                                table_id,
                                name,
                                local,
                                kind,
                                uuid)
                                values (?,?,?,?,?)""",
                                (table_id[0],
                                 i_name,
                                 index.fulltext,
                                 uni,
                                 str(uuid.uuid4())))

                    index_id = cur.execute("""SELECT dbd$indices.id from dbd$indices
                                            WHERE dbd$indices.name = :i_name""",
                                           {"i_name": i_name}).fetchone()
                    cur.execute(""" UPDATE dbd$indices
                                                SET name = NULL 
                                                WHERE name = '1'""")

                    for item in index.fields:
                        cur.execute(""" INSERT INTO dbd$index_details(
                                        index_id,
                                        position,
                                        field_id) values (?,?,?)""",
                                    (index_id[0], pos_i, -1))
                        cur.execute(""" UPDATE dbd$index_details
                                        SET field_id = (
                                        SELECT id from dbd$fields as field
                                        WHERE field.name = :field_n) 
                                        WHERE field_id = -1""",
                                    {"field_n": item})
                        if len(index.fields) != 1:
                            cur.execute(""" UPDATE dbd$index_details SET
                                            expression = :exp,
                                            descend = :desc
                                            WHERE index_id = :i_id""",
                                        {"exp": item.expression,
                                         "desc": item.desc,
                                         "i_id": index_id[0]})

                    pos_i += 1

            # Exceptions

            for table in self.schema.tables:
                pos_c = 0

                table_id = cur.execute("""SELECT id from dbd$tables
                                                    WHERE dbd$tables.name = :t_name""",
                                       {"t_name": table.name}).fetchone()
                for constraint in table.constraints:

                    if constraint.name != None:
                        c_name = constraint.name
                    else:
                        c_name = '1'

                    cur.execute(
                        """INSERT into dbd$constraints ( 
                        table_id,
                        name,
                        constraint_type,
                        reference,
                        has_value_edit,
                        cascading_delete,
                        expression,
                        uuid) values (?,?,?,?,?,?,?,?)""",
                        (table_id[0],
                         c_name,
                         constraint.kind,
                         -1,
                         constraint.has_value_edit,
                         constraint.cascading_delete,
                         constraint.expression,
                         str(uuid.uuid4())))

                    con_id = cur.execute("""SELECT con.id from dbd$constraints con
                                            WHERE con.name = :c_name""",
                                         {"c_name": c_name}).fetchone()
                    cur.execute(""" UPDATE dbd$constraints 
                                    SET name = NULL 
                                    WHERE name = '1'""")

                    for item in constraint.items:
                        cur.execute(""" INSERT INTO dbd$constraint_details(
                                                                   constraint_id, 
                                                                   position, 
                                                                   field_id) values (?,?,?)""",
                                    (con_id[0], pos_c, -1))
                        pos_c += 1
                        cur.execute(""" UPDATE dbd$constraint_details
                                        SET field_id = (
                                        SELECT id from dbd$fields as field
                                        WHERE field.name = :field_n) 
                                        WHERE field_id = -1""",
                                    {"field_n": item})

                    cur.execute(""" UPDATE dbd$constraints
                                    SET reference = (
                                    SELECT id from dbd$tables WHERE dbd$tables.name = :ref) 
                                    WHERE reference = -1""",
                                {"ref": constraint.reference})

            conn.commit()
            conn.close()

    def get_id(self, cursor, query):
        """
        Get all ids
        :param self:
        :return: map{name:id}
        """
        cursor.execute(query)
        result_map = {}
        for result_obj in self.get_result(cursor):
            result_map[result_obj["name"]] = result_obj["id"]
        return result_map

    def get_result(self, cursor):
        """
        Get result executing query
        :return:
        """
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results