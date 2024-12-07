import os
from config import *

# Create by Freddy Wicaksono, M.Kom
# Date : 07-12-2024

# Define the template for the PHP controller
php_template = """<?php
include_once('../models/{model_name}Model.php');

class {class_name}Controller
{
    private $model;

    public function __construct()
    {
        $this->model = new {model_name}Model();
    }

    public function add{class_name}({params})
    {
        return $this->model->add{class_name}({params});
    }

    public function get{class_name}($id)
    {
        return $this->model->get{class_name}($id);
    }

    public function Show($id)
    {
        $rows = $this->model->get{class_name}($id);
        foreach($rows as $row){
            $val = $row['nama'];
        }
        return $val;
    }

    public function update{class_name}($id, {params})
    {
        return $this->model->update{class_name}($id, {params});
    }

    public function delete{class_name}($id)
    {
        return $this->model->delete{class_name}($id);
    }

    public function get{class_name}List()
    {
        return $this->model->get{class_name}List();
    }
    
    public function getDataCombo()
    {
        return $this->model->getDataCombo();
    }
}
"""

# Define the data for the new entity
model_name = entity_name.capitalize()
class_name = entity_name.capitalize()

# Define the parameters and arguments
params_list = [f"${key}" for key in filter(lambda k: k != "id", field_list2.keys())]
params = ", ".join(params_list)
args = ", ".join(param[1:] for param in params_list)  # Remove the '$' for arguments

# Generate the PHP script
php_script = php_template.replace("{model_name}", model_name) \
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