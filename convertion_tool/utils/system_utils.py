import os


def delete_file_if_exist(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
