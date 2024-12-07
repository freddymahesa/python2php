import os
# Define the template for the PHP delete view
php_template = """<?php
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

# Define the data for the new entity
entity_name = "Dosen"
controller_name = "Dosen"
table_name = "dosen"

# Define the fields for the form (excluding 'id')
fields = {
    "nidn": {"type":"varchar","value":"string"},
    "nama": {"type":"varchar","value":"string"},
    "jk": {"type":"enum","value":"L,P"},
    "prodi": {"type":"enum","value":"Teknik Informatika,Sistem Informasi,Teknik Elektro"}
}

# Generate display fields
display_fields = ""
for field, details in fields.items():
    display_fields += f'''
                    <dt class="col-sm-3 font-medium text-gray-700">{field.capitalize()}:</dt>
                    <dd class="col-sm-9"><?php echo $row['{field}']; ?></dd>
    '''

# Generate the PHP script
php_script = php_template.replace("{entity_name}", entity_name) \
                         .replace("{controller_name}", controller_name) \
                         .replace("{table_name}", table_name) \
                         .replace("{display_fields}", display_fields)

folder_name = entity_name.lower()
os.makedirs(folder_name, exist_ok=True)

# Save the generated PHP script to a file
file_path = f"{folder_name}/{folder_name}_delete.php"
with open(file_path, "w") as file:
    file.write(php_script)

print(f"{file_path} has been generated successfully.")