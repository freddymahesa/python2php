import os
from config import *
from temp import *
import time

def run_controller():
    # Define the data for the new entity
    model_name = entity_name.capitalize()
    class_name = entity_name.capitalize()

    # Define the parameters and arguments
    params_list = [f"${key}" for key in filter(lambda k: k != "id", field_list2.keys())]
    params = ", ".join(params_list)
    args = ", ".join(param[1:] for param in params_list)  # Remove the '$' for arguments

    # Generate the PHP script
    php_script = con_template.replace("{model_name}", model_name) \
                            .replace("{class_name}", class_name) \
                            .replace("{params}", params) \
                            .replace("{args}", args)

    folder_name = 'controllers'
    controller_filename = entity_name.capitalize()

    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/{controller_filename}.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def run_model():
    # Define the data for the new entity
    class_name = entity_name.capitalize()
    table_name = entity_name.lower()


    # Define the parameters and their corresponding assignments
    params_list = [f"${field}" for field in field_list[1:]]
    col_list = [f"{field}" for field in field_list[1:]]
    params = ", ".join(params_list)
    columns = ", ".join(col_list)
    placeholders = ", ".join([f":{param[1:]}" for param in params_list])  # Remove the '$' for placeholders
    param_assignments = ",\n          ".join([f'":{param[1:]}" => {param}' for param in params_list])
    update_assignments = ", ".join([f"{param[1:]} = :{param[1:]}" for param in params_list])  # Remove the '$' for assignments

    # Generate the PHP script
    php_script = model_template.replace("{class_name}", class_name) \
                            .replace("{table_name}", table_name) \
                            .replace("{params}", params) \
                            .replace("{columns}", columns) \
                            .replace("{placeholders}", placeholders) \
                            .replace("{param_assignments}", param_assignments) \
                            .replace("{update_assignments}", update_assignments) \
                            .replace("{pk}", pk)

    folder_name = 'models'
    model_filename = entity_name.capitalize()

    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/{model_filename}Model.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def run_index():
    # Define the data for the new entity
    controller_name = entity_name.capitalize()

    # Define the fields for the table
    fields = field_list

    # Generate table headers
    table_headers = "\n".join([f'<th>{field}</th>' for field in fields])
    # Generate table data
    table_data = "\n".join([f'<td><?php echo $row["{field}"]; ?></td>' for field in fields])

    # Generate the PHP script
    php_script = index_template.replace("{entity_name}", entity_name) \
                            .replace("{controller_name}", controller_name) \
                            .replace("{table_headers}", table_headers) \
                            .replace("{table_data}", table_data)

    folder_name = entity_name.lower()
    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/index.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def run_add():
    # Define the data for the new entity
    controller_name = entity_name.capitalize()
    table_name = entity_name.lower()

    # Define the fields for the form
    fields = fields_without_id

    # Generate form processing code
    form_processing = "\n    ".join([f"${field} = $_POST['{field}'];" for field in fields.keys()])
    form_processing += "\n    // Insert the database record using your controller's method\n"
    form_processing += f"$dat = $obj->add{entity_name}(" + ", ".join([f"${field}" for field in fields.keys()]) + ");\n"
    form_processing += "$msg = getJSON($dat);"

    # Generate form fields
    form_fields = ""
    for field, details in fields.items():
        if details["type"] == "enum":
            # Split the value string into options
            options = details["value"].split(",")
            
            # Generate option HTML
            options_html = ''.join([f'<option value="{opt}">{opt}</option>' for opt in options])
            
            form_fields += f"""
                <div class="form-group">
                    <label>{field}:</label>
                    <select id="{field}" name="{field}" style="width:150px" class="form-control">
                        <option value="">--pilih--</option>
                        {options_html}
                    </select>
                </div>
            """
        else:  # Text inputs for other fields
            form_fields += f"""
                <div class="form-group">
                    <label>{field.capitalize()}:</label>
                    <input type="text" class="form-control" name="{field}"  />
                </div>
            """

    # Generate the PHP script
    php_script = add_template.replace("{entity_name}", entity_name) \
                            .replace("{controller_name}", controller_name) \
                            .replace("{form_processing}", form_processing) \
                            .replace("{form_fields}", form_fields) \
                            .replace("{table_name}", table_name)

    folder_name = entity_name.lower()
    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/add.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def run_edit():
    # Define the data for the new entity
    controller_name = entity_name.capitalize()
    table_name = entity_name.lower()

    # Define the fields for the form
    fields = field_list2

    # Generate form processing code
    form_processing = "\n    ".join([f"${field} = $_POST['{field}'];" for field in fields.keys()])
    form_processing += "\n    // Update the database record using your controller's method\n"
    form_processing += f"$dat = $obj->update{entity_name}(" + ", ".join([f"${field}" for field in fields.keys()]) + ");\n"
    form_processing += "$msg = getJSON($dat);"

    # Generate form fields
    form_fields = ""
    for field, details in fields.items():
        if details["type"] == "enum":
            # Split the value string into options
            options = details["value"].split(",")
            
            # Generate option HTML
            options_html = ''.join([f'<option value="{opt}">{opt}</option>' for opt in options])
            
            form_fields += f"""
                <div class="form-group">
                    <label>{field.capitalize()}:</label>
                    <select id="{field}" name="{field}" style="width:150px" 
                        class="form-control show-tick" required>
                    <option value="<?php echo $row['{field}']; ?>">
                    <?php echo $row['{field}']; ?></option>
                        {options_html}
                    </select>
                </div>
            """
        else:  # Text inputs for other fields
            if field == "id":
                form_fields += f"""
                    <div class="form-group">
                        <label>{field}:</label>
                        <input type="text" class="form-control" id="{field}" name="{field}" 
                            value="<?php echo $row['{field}']; ?>" readonly/>
                    </div>
                """
            else:
                form_fields += f"""
                    <div class="form-group">
                        <label>{field}:</label>
                        <input type="text" class="form-control" id="{field}" name="{field}" 
                            value="<?php echo $row['{field}']; ?>" />
                    </div>
                """

    # Generate the PHP script
    php_script = edit_template.replace("{entity_name}", entity_name) \
                            .replace("{controller_name}", controller_name) \
                            .replace("{form_processing}", form_processing) \
                            .replace("{form_fields}", form_fields) \
                            .replace("{table_name}", table_name)


    folder_name = entity_name.lower()
    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/edit.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def run_delete():
    # Define the data for the new entity
    controller_name = entity_name.capitalize()
    table_name = entity_name.lower()

    # Define the fields for the form (excluding 'id')
    fields = fields_with_id

    # Generate display fields
    display_fields = ""
    for field, details in fields.items():
        if(field == "id"):
            display_fields += f'''
                            <dt class="col-sm-3">{field.capitalize()}:</dt><dd class="col-sm-9"><?php echo $row['{field}']; ?></dd>
                            <input type="hidden" class="form-control" name="{field}" value="<?php echo $row['{field}']; ?>" readonly />
            '''
        else:

            display_fields += f'''
                            <dt class="col-sm-3">{field.capitalize()}:</dt><dd class="col-sm-9"><?php echo $row['{field}']; ?></dd>
            '''

    # Generate the PHP script
    php_script = del_template.replace("{entity_name}", entity_name) \
                            .replace("{controller_name}", controller_name) \
                            .replace("{table_name}", table_name) \
                            .replace("{display_fields}", display_fields) 
                            

    folder_name = entity_name.lower()
    # Save the generated PHP script to a file
    file_path = f"{project_path}/{folder_name}/delete.php"
    path = f"{project_path}/{folder_name}"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w") as file:
        file.write(php_script)

    print(f"{file_path} has been generated successfully.")

def main():
    start_time = time.time()
    run_model()
    time.sleep(1)
    run_controller()
    time.sleep(1)
    run_index()
    time.sleep(1)
    run_add()
    time.sleep(1)
    run_edit()
    time.sleep(1)
    run_delete()
    end_time = time.time()
    print(f"Time taken to generate files: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
