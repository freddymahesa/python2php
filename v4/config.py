from database import DatabaseConnection
from mod import *

entity_name = "dokter"

db = DatabaseConnection()
db.connect()

# Retrieve table fields
table_fields = db.get_table_fields(entity_name)

# Transform to the desired format
field_list = {}
for field in table_fields:
    # Handle different type transformations
    if 'int' in field['type']:
        field_type = 'int'
        value_type = 'int'
    elif 'varchar' in field['type']:
        field_type = 'varchar'
        value_type = 'string'
    elif 'enum' in field['type']:
        # For enum, extract the possible values
        field_type = 'enum'
        # Remove 'enum(' and ')' and split by comma, then remove quotes
        value_type = field['type'].replace('enum(', '').replace(')', '').replace('"', '').split(',')
        value_type = ','.join(value_type)
    else:
        # Default case
        field_type = field['type']
        value_type = field['type']
    
    field_list[field['name']] = {
        "type": field_type,
        "value": value_type
    }

# Clean up single quotes from enum values
field_list2 = clean_enum_values(field_list)

field_list = list(field_list2.keys())

fields_without_id = dict(list(field_list2.items())[1:])

pk ="id"

project_path="c:/xampp/htdocs/example"