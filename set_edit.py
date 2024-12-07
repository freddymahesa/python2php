import os
# Create by Freddy Wicaksono, M.Kom
# Date : 07-12-2024

# Define the template for the PHP view
php_template = """<?php
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

# Define the data for the new entity
entity_name = "Dosen"
controller_name = "Dosen"
table_name = "dosen"

# Define the fields for the form
fields = {
    "id": {"type":"int","value":"int"},
    "nidn": {"type":"varchar","value":"string"},
    "nama": {"type":"varchar","value":"string"},
    "jk": {"type":"enum","value":"L,P"},
    "prodi": {"type":"enum","value":"TIF,IND,PET"}
}

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
            <div class="mb-4">
                <label for="{field}" class="block text-sm font-medium text-gray-700">{field.capitalize()}:</label>
                <select id="{field}" name="{field}" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500" required>
                    <option value="<?php echo $row['{field}']; ?>"><?php echo $row['{field}']; ?></option>
                    {options_html}
                </select>
            </div>
        """
    else:  # Text inputs for other fields
        form_fields += f"""
            <div class="mb-4">
                <label for="{field}" class="block text-sm font-medium text-gray-700">{field.capitalize()}:</label>
                <input type="text" id="{field}" name="{field}" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500" value="<?php echo $row['{field}']; ?>" required />
            </div>
        """

# Generate the PHP script
php_script = php_template.replace("{entity_name}", entity_name) \
                         .replace("{controller_name}", controller_name) \
                         .replace("{form_processing}", form_processing) \
                         .replace("{form_fields}", form_fields) \
                         .replace("{table_name}", table_name)


folder_name = entity_name.lower()
os.makedirs(folder_name, exist_ok=True)

# Save the generated PHP script to a file
file_path = f"{folder_name}/{folder_name}_edit.php"
with open(file_path, "w") as file:
    file.write(php_script)

print(f"{file_path} has been generated successfully.")