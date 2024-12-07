con_template = """<?php
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

model_template = """<?php

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

index_template = """<?php
include("../controllers/{controller_name}.php");
include("../lib/functions.php");
$obj = new {controller_name}Controller();
$rows = $obj->get{entity_name}List();
?>
<html>
<head>
    <title>{entity_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 class="text-3xl font-bold mb-2">{entity_name}</h1>
        <p class="text-gray-600 mb-4">List All Data</p>
        <a style="margin:10px 0px;" class="bg-blue-500 text-white px-2 py-1 rounded mr-2" href="add.php"><i class="fas fa-plus"></i> Create New Data</a>
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-gray-200">
                <thead>
                    <tr>
                        {table_headers}
                        <th class="py-2 px-4 border-b">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach($rows as $row){ ?>
                    <tr class="bg-gray-100">
                        {table_data}
                        <td class="py-2 px-4 border-b">
                        <a class="bg-blue-500 text-white px-2 py-1 rounded mr-2" href="edit.php?id=<?php echo $row['id']; ?>"><i class="fas fa-pen"></i></a>
                        <a class="bg-red-500 text-white px-2 py-1 rounded" href="delete.php?id=<?php echo $row['id']; ?>"><i class="fas fa-trash"></i></a>
                        </td>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

edit_template = """<?php
include("../controllers/{controller_name}.php");
include("../lib/functions.php");
$obj = new {controller_name}Controller();
$msg = null;
if (isset($_GET["id"])) {
    $id = $_GET["id"];
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Form was submitted, process the update here
    {form_processing}
}
$rows = $obj->get{entity_name}($id);
?>
<html>
<head>
    <title>Edit {entity_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 class="text-3xl font-bold mb-2">{entity_name}</h1>
        <p class="text-gray-600 mb-4">Edit Data</p>

        <?php 
        if ($msg === true) { 
            echo '<div class="bg-green-500 text-white p-3 rounded mb-4">Update Data Berhasil</div>';
            echo '<meta http-equiv="refresh" content="2;url='.base_url().'{table_name}/">';
        } elseif ($msg === false) {
            echo '<div class="bg-red-500 text-white p-3 rounded mb-4">Update Gagal</div>'; 
        }
        ?>

        <div class="flex items-center mb-4">
            <i class="fas fa-user-edit fa-4x mr-4"></i>
            <h2 class="text-xl font-semibold">Edit Data {entity_name}</h2>
        </div>
        <hr class="mb-4"/>

        <form name="formEdit" method="POST" action="">
            <input type="hidden" name="submitted" value="1"/>
            <?php foreach ($rows as $row): ?>
            {form_fields}
            <?php endforeach; ?>
            <div class="flex justify-between">
                <button class="bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600" type="submit">Save</button>
                <a href="#index" class="bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded hover:bg-gray-400">Cancel</a>
            </div>
        </form>
    </div>
</body>
</html>
"""

del_template = """<?php
include("../controllers/{controller_name}.php");
include("../lib/functions.php");
$obj = new {controller_name}Controller();

if (isset($_GET["id"])) {
    $id = $_GET["id"];
}

$msg = null;
if (isset($_POST['submitted']) && $_SERVER['REQUEST_METHOD'] == 'POST') {
    // Delete the record using the controller method
    $dat = $obj->delete{entity_name}($id);
    $msg = getJSON($dat);
}

$rows = $obj->get{entity_name}($id);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete {entity_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 class="text-3xl font-bold mb-2">{entity_name}</h1>
        <p class="text-gray-600 mb-4">Delete Data</p>

        <?php 
        if ($msg === true) { 
            echo '<div class="bg-green-500 text-white p-3 rounded mb-4">Delete Data Berhasil</div>';
            echo '<meta http-equiv="refresh" content="3;url='.base_url().'{table_name}/">';
        } elseif ($msg === false) {
            echo '<div class="bg-red-500 text-white p-3 rounded mb-4">Delete Gagal</div>'; 
        }
        ?>

        <div class="flex items-center mb-4">
            <i class="fas fa-user-times fa-4x mr-4"></i>
            <h2 class="text-xl font-semibold">Delete Data {entity_name}</h2>
        </div>
        <hr class="mb-4"/>

        <form name="formDelete" method="POST" action="">
            <input type="hidden" name="submitted" value="1"/>
            <input type="hidden" name="id" value="<?php echo $row['id']; ?>" readonly />
            
            <dl class="row mt-1">
                <?php foreach ($rows as $row): ?>
                    {display_fields}
                <?php endforeach; ?>
            </dl>
            
            <div class="flex justify-between mt-4">
                <button class="bg-red-500 text-white font-semibold py-2 px-4 rounded hover:bg-red-600" type="submit">Delete</button>
                <a href="#index" class="bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded hover:bg-gray-400">Cancel</a>
            </div>
        </form>
    </div>
</body>
</html>
"""

add_template = """<?php
include("../controllers/{controller_name}.php");
include("../lib/functions.php");
$obj = new {controller_name}Controller();
$msg = null;
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Form was submitted, process the update here
    {form_processing}
}
?>
<html>
<head>
    <title>{entity_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 class="text-3xl font-bold mb-2">{entity_name}</h1>
        <p class="text-gray-600 mb-4">Entry Data</p>

        <?php 
        if ($msg === true) { 
            echo '<div class="bg-green-500 text-white p-3 rounded mb-4">Insert Data Berhasil</div>';
            echo '<meta http-equiv="refresh" content="2;url='.base_url().'{table_name}/">';
        } elseif ($msg === false) {
            echo '<div class="bg-red-500 text-white p-3 rounded mb-4">Insert Gagal</div>'; 
        }
        ?>

        <div class="flex items-center mb-4">
            <i class="fas fa-user-graduate fa-4x mr-4"></i>
            <h2 class="text-xl font-semibold">Add New Data</h2>
        </div>
        <hr class="mb-4"/>

        <form name="formAdd" method="POST" action="">
            {form_fields}
            <div class="flex justify-between">
                <button class="bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600" type="submit">Save</button>
                <a href="#index" class="bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded hover:bg-gray-400">Cancel</a>
            </div>
        </form>
    </div>
</body>
</html>
"""