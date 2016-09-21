import re

from container.tag import Tag
from util import file_utils


class FilesController:
    def __init__(self, project_path, files, language):
        self.project_path = project_path
        self.files = files
        self.language = language
        self.tags = {}
        self.deleted_files = []
        self.none_tagged_files = []
        self.test_files = []

    def parse(self, fun_is_file_exists, fun_get_tags_from_file):
        for file in self.files:
            if not fun_is_file_exists(file_utils.get_system_file_path(self.project_path, file.file_path)):
                self.deleted_files.append(file)
            else:
                if is_test_file(file):
                    self.test_files.append(file)
                else:
                    if get_file_extension(file) == self.language['extension']:
                        tags = fun_get_tags_from_file(file.file_content,
                                                      self.language['regex'],
                                                      self.language['start'],
                                                      self.language['end'],
                                                      self.language['divider'],
                                                      self.language['ignore'])
                        if tags.__len__() != 0:
                            put_tags_to_map(self.tags, tags, file)
                        else:
                            self.none_tagged_files.append(file)

        match_test_files_to_files_in_tags(self.tags, self.test_files)


def get_file_extension(file):
    return file.file_path.split('.')[-1]


def match_test_files_to_files_in_tags(tags, test_files):
    for tag in tags.values():
        for file in tag.files:
            for test_file in test_files:
                if is_test_file_valid(file, test_file):
                    file.test_file = test_file
                    break
                else:
                    file.test_file = None


def is_test_file_valid(file, test_file):
    return get_file_name_without_extension(file) == get_file_name_without_extension(test_file).replace('Test', '')


def get_file_name_without_extension(file):
    file_name = file.file_path.split('/')[-1]
    return file_name.rpartition('.')[0]


def sort(map, reverse):
    return sorted(map.items(), key=lambda x: x[1].get_files_count(), reverse=reverse)


def is_test_file(file):
    return file.file_path.find('Test') != -1


def put_tags_to_map(tags_map, tags, diff_file):
    for tag in tags:
        if tag in tags_map:
            tags_map[tag].add_file(diff_file)
        else:
            tags_map[tag] = Tag([diff_file])


def get_tags_from_file(file_content, regex, start, end, divider, ignore):
    empty_str = ''

    try:
        annotation_tags = re \
            .search(regex, file_content, re.DOTALL) \
            .group(0) \
            .replace(start, empty_str) \
            .replace(end, empty_str)
    except AttributeError:
        return []

    for i in ignore:
        annotation_tags = annotation_tags.replace(i, empty_str)
    if annotation_tags.find(divider) != -1:
        annotation_tags = annotation_tags \
            .replace(' ', empty_str) \
            .replace('\n', empty_str)
        return annotation_tags.split(divider)
    else:
        return [annotation_tags]


def add_tags_to_existing_map(existing_map, new_map):
    for new_key in new_map.keys():
        if new_key in existing_map:
            add_new_files_to_existing_map(existing_map, new_key, new_map)
        else:
            existing_map[new_key] = new_map[new_key]


def add_new_files_to_existing_map(existing_map, new_key, new_map):
    for new_file in new_map[new_key].files:
        if new_file not in existing_map[new_key].files:
            existing_map[new_key].add_file(new_file)
