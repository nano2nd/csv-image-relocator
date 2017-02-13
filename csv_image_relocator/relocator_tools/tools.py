import os


def is_valid_str(file_name):
    return bool(file_name)


def is_na(file_name):
    return file_name.lower() == 'na'


def search_file(filename_part, directory):
    for file in os.listdir(directory):
        if filename_part in file:
            return file

    raise FileNotFoundError
