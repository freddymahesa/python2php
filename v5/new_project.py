from mod import *
from config import *
import os
import time

a = is_path_not_empty(project_path)
b = is_path_exsist(project_path)

if(b==False):
    os.makedirs(project_path, exist_ok=True)
    time.sleep(1)
    extract_zip('data/example.zip', project_path)
    print(f"New Project is now ready in: {project_path}")
else:
    if(len(a) == 0):
        extract_zip('data/example.zip', project_path)
        print(f"New Project is now ready in: {project_path}")
    else:
        print("Project path is not empty, new project failed!")