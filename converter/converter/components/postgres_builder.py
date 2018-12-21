import psycopg2 as pg

class Postgres_builder:

    def __init__(self, schema):
        self.schema = schema

    def generate_db(self, db_name):
        self.create_db(db_name)
        conn = pg.connect(database=db_name, user="postgres", password="123", host="localhost", port="5432")
        cur = conn.cursor()
        conn.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cur.execute('DROP SCHEMA IF EXISTS "{}" CASCADE'
                    .format(self.schema.name))
        cur.execute('CREATE SCHEMA "{}"'
                    .format(self.schema.name))

        for domain in self.schema.domains:
            cur.execute('CREATE DOMAIN "{}"."{}" AS "{}"'.format(
                self.schema.name,
                domain.name,
                self.schema(domain.type)))

        for table in self.schema.tables:
            request = ('CREATE TABLE "{}"."{}" ('.format(
                self.schema.name,
                table.name))

            fields = []
            primary = []
            unique = []
            checks = []

            for field in table.fields:
                fields.append('"{}" "{}"."{}"'.format(
                    field.name,
                    self.schema.name,
                    field.domain))
            for constraint in table.constraints:
                if 'PRIMARY' == constraint.kind:
                    primary.append(constraint.items[0])
                elif 'UNIQUE' == constraint.kind:
                    unique.append(constraint.items[0])
                elif 'CHECK' == constraint.kind:
                    check = constraint.expression.replace('[', '')
                    check = check.replace(']', '')
                    checks.append('CHECK {}'.format(check))
            if primary != []:
                fields.append('PRIMARY KEY (\"{}\")'.format(', '.join(primary)))
            if unique != []:
                fields.append('UNIQUE (\"{}\")'.format(', '.join(unique)))
            if checks != []:
                fields += checks
            request += (', '.join(fields))
            request += ');'
            cur.execute(request)

        for table in self.schema.tables:
            for constraint in table.constraints:
                if constraint.kind == 'FOREIGN':
                    request_c = 'ALTER TABLE "{}"."{}" ADD {} FOREIGN KEY ("{}") REFERENCES "{}"."{}" ON DELETE '.format(
                        self.schema.name,
                        table.name,
                        "CONSTRAINT " + constraint.name if constraint.name != None else "",
                        constraint.items[0],
                        self.schema.name,
                        constraint.reference)
                    if constraint.cascading_delete:
                        request_c += ' CASCADE;'
                    elif not constraint.cascading_delete:
                        request_c += ' RESTRICT;'
                    elif constraint.cascading_delete == None:
                        request_c += ' SET NULL;'
                    cur.execute(request_c)

        for table in self.schema.tables:
            for index in table.indices:
                cur.execute('CREATE {} INDEX {} ON "{}"."{}" ("{}");'.format(
                    "UNIQUE" if index.uniqueness else "",
                    index.name if index.name != None else "",
                    self.schema.name,
                    table.name, index.fields[0]))d

        conn.commit()
        conn.close()

    def create_db(db_name):
        conn = pg.connect(user="postgres", password="123", host="localhost", port="5432")
        cur = conn.cursor()
        conn.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute('DROP DATABASE IF EXISTS ' + db_name)
        cur.execute('CREATE DATABASE ' + db_name)
        conn.commit()
        conn.close()

def get_type(d_type):
    if d_type in pg_types:
        return pg_types[d_type]

pg_types = dict(
        INTEGER="int",
        BLOB="bytea",
        BOOLEAN="bool",
        BYTE="int2",
        LARGEINT="int8",
        SMALLINT="int2",
        WORD="int2",
        DATE="date",
        TIME="time",
        MEMO="text",
        FLOAT="numeric",
        STRING="varchar",
        CODE="varchar"
    )