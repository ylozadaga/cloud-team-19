import os


def is_file_exist(file_path):
    return os.path.exists(file_path)


def delete_file_if_exist(file_path):
    if is_file_exist(file_path):
        os.remove(file_path)
        return True
    else:
        return False
