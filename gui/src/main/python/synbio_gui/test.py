import os

project_root = os.environ.get('PYTHONPATH')
print(project_root)
project_root = project_root.split(os.path.pathsep)[1]
print(project_root)
print("pathsep:", os.path.pathsep, "end")