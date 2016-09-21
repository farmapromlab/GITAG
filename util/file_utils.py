import mmap
import os.path


def get_file_content(project_path, file_path):
    system_file_path = get_system_file_path(project_path, file_path)
    if is_file_exists(system_file_path):
        diff_file = open(system_file_path)
        return mmap.mmap(diff_file.fileno(), 0, access=mmap.ACCESS_READ)
    else:
        return None


def is_file_exists(system_file_path):
    return os.path.isfile(system_file_path)


def get_system_file_path(project_path, file_path):
    return project_path + '/' + file_path
