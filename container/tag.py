class Tag:
    def __init__(self, files):
        self.files = files

    def get_files_count(self):
        return self.files.__len__()

    def add_file(self, file_name):
        self.files.append(file_name)

    @property
    def files(self):
        return self.files

    @files.setter
    def files(self, files):
        self.files = files

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
