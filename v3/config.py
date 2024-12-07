entity_name = "Jadwal"

field_list2 = {
    "id": {"type":"int","value":"int"},
    "kodemk": {"type":"varchar","value":"string"},
    "matakuliah": {"type":"varchar","value":"string"},
    "kelas": {"type":"varchar","value":"string"},
    "hari": {"type":"varchar","value":"string"},
    "waktu":{"type":"varchar","value":"string"},
    "ruangan": {"type":"varchar","value":"string"},
    "dosen": {"type":"varchar","value":"string"},
}

field_list = list(field_list2.keys())

fields_without_id = dict(list(field_list2.items())[1:])

pk ="id"

project_path="c:/xampp/htdocs/example"