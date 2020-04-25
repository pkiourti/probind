import os


def get_saved_models():
    """
    :return: a python list of all saved models. By convention all models are saved under models/.
    """
    return os.listdir('models')


def delete_model(name):
    """
    :args name: a string indicating which model to delete
    :return:
    """
    file_to_remove = os.path.join('models', name)
    try:
        os.remove(file_to_remove)
    except FileNotFoundError as e:
        print(f'File {name} is not deleted. {e}')


def data_files(data_dir_filepath):
    i = 1
    while os.path.exists(os.path.join(data_dir_filepath, 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists(data_dir_filepath):
        os.makedirs(data_dir_filepath)

    return (os.path.join(data_dir_filepath, 'x_forward_' + str(i)),
            os.path.join(data_dir_filepath, 'x_reverse_' + str(i)),
            os.path.join(data_dir_filepath, 'y_' + str(i)))

