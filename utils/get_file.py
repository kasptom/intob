import os

from root_dir import ROOT_DIR


def full_path(relative_file_path: str):
    if not relative_file_path.startswith("/"):
        relative_file_path = "/" + relative_file_path
    return ROOT_DIR + relative_file_path


def create_file_and_folders_if_not_exist(full_directory_path: str):
    os.makedirs(os.path.dirname(full_directory_path), exist_ok=True)
