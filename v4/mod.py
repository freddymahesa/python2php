import json
import re

def display_fields_json_style(field_list):
    print(json.dumps(field_list, indent=2))

def clean_enum_values(field_list):
    for field, details in field_list.items():
        if details['type'] == 'enum':
            # Remove single quotes using regex
            details['value'] = re.sub(r"'", "", details['value'])
    return field_list