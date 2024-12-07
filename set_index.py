import os
# Define the template for the PHP view
php_template = """<?php
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

# Define the data for the new entity
entity_name = "Dosen"
controller_name = "Dosen"

# Define the fields for the table
fields = ["id", "nidn", "nama", "jk", "prodi"]

# Generate table headers
table_headers = "\n".join([f'<th class="py-2 px-4 border-b">{field}</th>' for field in fields])
# Generate table data
table_data = "\n".join([f'<td class="py-2 px-4 border-b"><?php echo $row["{field}"]; ?></td>' for field in fields])

# Generate the PHP script
php_script = php_template.replace("{entity_name}", entity_name) \
                         .replace("{controller_name}", controller_name) \
                         .replace("{table_headers}", table_headers) \
                         .replace("{table_data}", table_data)

folder_name = entity_name.lower()
os.makedirs(folder_name, exist_ok=True)

# Save the generated PHP script to a file
file_path = f"{folder_name}/{folder_name}_index.php"
with open(file_path, "w") as file:
    file.write(php_script)

print(f"{file_path} has been generated successfully.")