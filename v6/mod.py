import json
import re
import os
import zipfile

def display_fields_json_style(field_list):
    print(json.dumps(field_list, indent=2))

def clean_enum_values(field_list):
    for field, details in field_list.items():
        if details['type'] == 'enum':
            # Remove single quotes using regex
            details['value'] = re.sub(r"'", "", details['value'])
    return field_list

def process_table_fields(db, entity_name):
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
    
    return field_list

def extract_zip(zip_path, extract_path=None):
    # If no extract path is provided, use the directory of the zip file
    if extract_path is None:
        extract_path = os.path.dirname(zip_path)
    
    # Create the extraction directory if it doesn't exist
    os.makedirs(extract_path, exist_ok=True)
    
    try:
        # Open the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all contents to the specified path
            zip_ref.extractall(extract_path)
        
        print(f"Successfully extracted {zip_path} to {extract_path}")
        return extract_path
    
    except zipfile.BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")
        return None
    
    except PermissionError:
        print(f"Error: Permission denied. Cannot extract to {extract_path}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def is_path_not_empty(path):
    # Check if path exists and is not an empty directory
    return os.path.exists(path) and os.listdir(path)

def is_path_exsist(path):
    # Check if path exists and is not an empty directory
    return os.path.exists(path) 