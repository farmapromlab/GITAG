class File:
    def __init__(self, file_path, file_content, added_lines, deleted_lines):
        self.file_path = file_path
        self.file_content = file_content
        self.added_lines = added_lines
        self.deleted_lines = deleted_lines
        self.lines = self.get_file_lines()
        self.test_file = None

    @property
    def file_path(self):
        return self.file_path

    @file_path.setter
    def file_path(self, file_path):
        self.file_path = file_path

    @property
    def file_content(self):
        return self.file_content

    @file_content.setter
    def file_content(self, file_content):
        self.file_content = file_content

    @property
    def added_lines(self):
        return self.added_lines

    @added_lines.setter
    def added_lines(self, added_lines):
        self.added_lines = added_lines

    @property
    def deleted_lines(self):
        return self.deleted_lines

    @deleted_lines.setter
    def deleted_lines(self, deleted_lines):
        self.deleted_lines = deleted_lines

    @property
    def lines(self):
        return self.lines

    @lines.setter
    def lines(self, lines):
        self.lines = lines

    @property
    def test_file(self):
        return self.test_file

    @test_file.setter
    def test_file(self, test_file):
        self.test_file = test_file

    def get_added_files_percent(self):
        return round(float(float(100) * float(self.added_lines) / float(self.lines)), 2) \
            if self.lines != 0 \
            else 0

    def get_deleted_files_percent(self):
        return round(float(float(100) * float(self.deleted_lines) / float(self.lines)), 2) \
            if self.lines != 0 \
            else 0

    def get_status(self):
        if self.lines is not 0:
            return 'Added' if self.get_added_files_percent() == 100 else 'Modified'

    def get_file_lines(self):
        if self.file_content is None:
            return 0
        else:
            lines_count = 0
            for _ in iter(self.file_content.readline, ''):
                lines_count += 1
            return lines_count

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
