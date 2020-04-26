import os

project_root = os.environ.get('PYTHONPATH')
print(project_root)

def check_avail_model_name(model_name):
    '''
    Checks if input model_name already exists in /models folder.
    Assumes that all files in /models folder have the appropriate file extension and should be checked against.
    Returns True or False.
    '''
    exists = False
    models_path = os.path.join(project_root, 'models')  # synbio_gui/python/main/src/gui/models

    if not os.path.exists(models_path):
        os.makedirs(models_path)

    # list of file names without extensions, e.g. "test1.txt" --> "test1"
    model_files = [os.path.splitext(os.path.basename(os.path.join(models_path, f)))[0] \
                   for f in os.listdir(models_path) if os.path.isfile(os.path.join(models_path, f))]

    try:
        exists_idx = model_files.index(model_name)
    except ValueError:
        exists_idx = -1

    if (exists_idx >= 0):
        exists = True

    return exists

if __name__ == '__main__':
    name_exists = check_avail_model_name('test')
    i = 1
    while (name_exists == True):
        new_name = 'test' + "_" + str(i)
        print(new_name)
        name_exists = check_avail_model_name(new_name)
        print(name_exists)
        i += 1


    print(new_name)