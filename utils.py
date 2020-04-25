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

