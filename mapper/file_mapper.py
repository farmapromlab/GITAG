from container.file import File


class FileMapper:
    def __init__(self, diff):
        self.diff = diff

    def map_files(self, project_path, fun_get_file_content):
        array = self.diff.split('\n')
        array.pop()

        files = []
        for line in array:
            args = line.split('\t')
            file_path = args[2]
            file_content = fun_get_file_content(project_path, file_path)
            added_lines = 0 if args[0] == '-' else int(args[0])
            deleted_lines = 0 if args[1] == '-' else int(args[1])
            files.append(File(file_path, file_content, added_lines, deleted_lines))

        return files
