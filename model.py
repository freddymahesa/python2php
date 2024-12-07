
import os 
# Define the template for the PHP model
php_template = """<?php

include_once('../db/database.php');

class {class_name}Model
{
    private $db;

    public function __construct()
    {
        $this->db = new Database();
    }

    public function add{class_name}({params})
    {
        $sql = "INSERT INTO {table_name} ({columns}) VALUES ({placeholders})";
        $params = array(
          {param_assignments}
        );

        $result= $this->db->executeQuery($sql, $params);
        // Check if the insert was successful
        if ($result) {
            $response = array(
                "success" => true,
                "message" => "Insert successful"
            );
        } else {
            $response = array(
                "success" => false,
                "message" => "Insert failed"
            );
        }
    
        // Return the response as JSON
        return json_encode($response);
    }

    public function get{class_name}($id)
    {
        $sql = "SELECT * FROM {table_name} WHERE {pk} = :id";
        $params = array(":id" => $id);

        return $this->db->executeQuery($sql, $params)->fetchAll(PDO::FETCH_ASSOC);
    }

    public function update{class_name}($id, {params})
    {
        $sql = "UPDATE {table_name} SET {update_assignments} WHERE {pk} = :id";
        $params = array(
          {param_assignments},
          ":id" => $id
        );
    
        // Execute the query
        $result = $this->db->executeQuery($sql, $params);
    
        // Check if the update was successful
        if ($result) {
            $response = array(
                "success" => true,
                "message" => "Update successful"
            );
        } else {
            $response = array(
                "success" => false,
                "message" => "Update failed"
            );
        }
    
        // Return the response as JSON
        return json_encode($response);
    }
    

    public function delete{class_name}($id)
    {
        $sql = "DELETE FROM {table_name} WHERE {pk} = :id";
        $params = array(":id" => $id);

        $result = $this->db->executeQuery($sql, $params);
        // Check if the delete was successful
        if ($result) {
            $response = array(
                "success" => true,
                "message" => "Delete successful"
            );
        } else {
            $response = array(
                "success" => false,
                "message" => "Delete failed"
            );
        }
    
        // Return the response as JSON
        return json_encode($response);
    }

    public function get{class_name}List()
    {
        $sql = 'SELECT * FROM {table_name} limit 100';
        return $this->db->query($sql)->fetchAll(PDO::FETCH_ASSOC);
    }

    public function getDataCombo()
    {
        $sql = 'SELECT * FROM {table_name}';
        $data = array();
        $data = $this->db->query($sql)->fetchAll(PDO::FETCH_ASSOC);
        header('Content-Type: application/json');
        echo json_encode($data);
    }
}
"""

# Define the data for the new entity
entity_name = "Dosen"
class_name = "Dosen"
table_name = "dosen"
pk ="id"

# Define the parameters and their corresponding assignments
params_list = ["$nidn", "$nama", "$jk", "$prodi"]
params = ", ".join(params_list)
columns = ", ".join(["nidn", "nama", "jk", "prodi"])
placeholders = ", ".join([f":{param[1:]}" for param in params_list])  # Remove the '$' for placeholders
param_assignments = ",\n          ".join([f'"{param} => {param}"' for param in params_list])
update_assignments = ", ".join([f"{param[1:]} = :{param[1:]}" for param in params_list])  # Remove the '$' for assignments

# Generate the PHP script
php_script = php_template.replace("{class_name}", class_name) \
                         .replace("{table_name}", table_name) \
                         .replace("{params}", params) \
                         .replace("{columns}", columns) \
                         .replace("{placeholders}", placeholders) \
                         .replace("{param_assignments}", param_assignments) \
                         .replace("{update_assignments}", update_assignments) \
                         .replace("{pk}", pk)

folder_name = 'models'
model_filename = entity_name.capitalize()
os.makedirs(folder_name, exist_ok=True)

# Save the generated PHP script to a file
file_path = f"{folder_name}/{model_filename}Model.php"
with open(file_path, "w") as file:
    file.write(php_script)

print(f"{file_path} has been generated successfully.")