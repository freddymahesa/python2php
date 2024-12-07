import os
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
        return $this->model->add{class_name}({args});
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
        return $this->model->update{class_name}($id, {args});
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
entity_name = "Dosen"
model_name = "Dosen"
class_name = "Dosen"

# Define the parameters and arguments
params_list = ["$nidn", "$nama", "$jk", "$prodi"]
params = ", ".join(params_list)
args = ", ".join(param[1:] for param in params_list)  # Remove the '$' for arguments

# Generate the PHP script
php_script = php_template.replace("{model_name}", model_name) \
                         .replace("{class_name}", class_name) \
                         .replace("{params}", params) \
                         .replace("{args}", args)

folder_name = 'controllers'
controller_filename = entity_name.capitalize()
os.makedirs(folder_name, exist_ok=True)

# Save the generated PHP script to a file
file_path = f"{folder_name}/{controller_filename}.php"
with open(file_path, "w") as file:
    file.write(php_script)

print(f"{file_path} has been generated successfully.")