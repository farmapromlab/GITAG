#!/usr/bin/env python

import json
import sys

from controller import files_controller
from controller.files_controller import FilesController
from git.git_repo import GitRepo
from mapper.file_mapper import FileMapper
from report import html_reporter
from util import file_utils


def main():
    try:
        validate_args(sys.argv)

        project_path = sys.argv[1]
        branch_1 = sys.argv[2]
        branch_2 = sys.argv[3]
        config = sys.argv[4]

        git_repo = GitRepo(project_path)
        is_stashed = git_repo.stash()
        current_branch = git_repo.get_current_branch()
        git_repo.checkout_to_branch(branch_2)
        diff = git_repo.diff_versions(branch_1, branch_2)

        file_mapper = FileMapper(diff)
        files = file_mapper.map_files(project_path, file_utils.get_file_content)

        tags = {}
        deleted_files = []
        none_tagged_files = []
        config = json.load(open(config))
        languages = config['languages']
        for language in languages:
            controller = FilesController(project_path, files, language)
            controller.parse(file_utils.is_file_exists, files_controller.get_tags_from_file)

            files_controller.add_tags_to_existing_map(tags, controller.tags)
            deleted_files += controller.deleted_files
            none_tagged_files += controller.none_tagged_files

        html_reporter.generate_tag_report(project_path,
                                          files_controller.sort(tags, True),
                                          deleted_files,
                                          none_tagged_files,
                                          branch_1,
                                          branch_2)

        git_repo.checkout_to_branch(current_branch)

        if is_stashed:
            git_repo.stash_pop()

        if none_tagged_files.__len__() != 0:
            for file in none_tagged_files:
                print file.file_path
            sys.exit('Untagged files! Build Failed')

    except IndexError:
        print ''


def validate_args(args):
    if args.__len__() != 5:
        sys.exit('You need to provide 4 arguments: [GIT_PROJECT_PATH] [branch_without_changes] [branch_with_changes] [config_file]')

if __name__ == '__main__':
    main()
