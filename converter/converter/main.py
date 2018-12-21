# import xdb2dbd,dbd2xdb,generate_db
import components.loader
import xml.dom.minidom as md

import dbd_to_xml, xml_to_dbd

import sys

reload(sys)
sys.setdefaultencoding('utf8')


xdb_s = "components/data/prjadm.xdb"
dbd_r = "result.db"
xdb_r = "result.xdb"
pg_name = "db_metadata"

xml_to_dbd.parse(xdb_s, dbd_r)
dbd_to_xml.parse(dbd_r, xdb_r)