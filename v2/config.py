entity_name = "Matakuliah"

field_list2 = {
    "id": {"type":"int","value":"int"},
    "kodemk": {"type":"varchar","value":"string"},
    "namamk": {"type":"varchar","value":"string"},
    "sks": {"type":"int","value":"int"},
    "prodi": {"type":"enum","value":"TIF,IND,PET"}
}

field_list = list(field_list2.keys())

fields_without_id = dict(list(field_list2.items())[1:])

pk ="id"

project_path="c:/xampp/htdocs/example"