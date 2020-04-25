import os

project_root = os.environ.get('PYTHONPATH')
project_root = project_root.split(os.path.pathsep)[1]

def get_saved_models():
    """
    :return: a python list of all saved models. By convention all models are saved under models/.
    """
    return os.listdir(os.path.join(project_root, 'models'))


def delete_model(file_to_remove):
    """
    :args name: a string indicating which model to delete
    :return:
    """
    try:
        os.remove(file_to_remove)
        return True, None
    except Exception as e:
        print(f'File is not deleted. {e}')
        return False, e


def data_files(data_dir_filepath):
    i = 1
    while os.path.exists(os.path.join(data_dir_filepath, 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists(data_dir_filepath):
        os.makedirs(data_dir_filepath)

    return (os.path.join(data_dir_filepath, 'x_forward_' + str(i)),
            os.path.join(data_dir_filepath, 'x_reverse_' + str(i)),
            os.path.join(data_dir_filepath, 'y_' + str(i)))


def rename(new_name, old_name):
    try:
        os.rename(old_name, new_name)
        return True, None
    except Exception as e:
        print(f'File not renamed. {e}')
        return False, e
