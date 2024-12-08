from database import DatabaseConnection
from mod import *

# -----------Edit here-----------------
# table name
entity_name = "matakuliah"         

# -------------------------------------
db = DatabaseConnection()
db.connect()

# Assuming db and entity_name are already defined
field_list = process_table_fields(db, entity_name)

# Clean up single quotes from enum values
field_list2 = clean_enum_values(field_list)

field_list = list(field_list2.keys())

fields_without_id = dict(list(field_list2.items())[1:])
fields_with_id = dict(list(field_list2.items()))

pk = db.get_primary_key(entity_name)