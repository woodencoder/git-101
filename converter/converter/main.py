# import xdb2dbd,dbd2xdb,generate_db
import components.loader
import xml.dom.minidom as md

import dbd_to_xml, xml_to_dbd
from components import  loader, postgres_builder

import sys

reload(sys)
sys.setdefaultencoding('utf8')


xdb_s = "components/data/prjadm.xdb"
dbd_r = "result.db"
xdb_r = "result.xdb"
pg_name = "metadata_db"

xml_to_dbd.parse(xdb_s, dbd_r)
dbd_to_xml.parse(dbd_r, xdb_r)

schema = loader.Loader(dbd_r).dbd_to_ram()
postgres_builder = postgres_builder.Postgres_builder(schema)
postgres_builder.generate_db(pg_name)