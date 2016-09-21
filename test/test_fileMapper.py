from unittest import TestCase

from mapper.file_mapper import FileMapper
from container.file import File


class TestFileMapper(TestCase):
    def test_get_files_from_diff_should_return_four_files(self):
        diff = '4\t0\t.gitignore\n' \
               '8\t8\tIZIFarmaProm/build.gradle\n' \
               '1\t1\tIZIFarmaProm/src/dev/res/values/strings.xml\n' \
               '2\t6\tIZIFarmaProm/src/main/AndroidManifest.xml\n' \
               ' '
        file_mapper = FileMapper(diff)
        actual = file_mapper.map_files('', get_file_content_mock)

        self.assertEqual(4, actual.__len__())

    def test_get_files_from_diff_should_return_correct_array(self):
        diff = '4\t0\t.gitignore\n' \
               ' '
        file_mapper = FileMapper(diff)
        diffed_files = file_mapper.map_files('', get_file_content_mock)
        actual = diffed_files[0]
        expected = File('.gitignore', None, 4, 0)

        self.assertEqual(expected.file_path, actual.file_path)
        self.assertEqual(expected.deleted_lines, actual.deleted_lines)
        self.assertEqual(expected.added_lines, actual.added_lines)


def get_file_content_mock(project_path, file_path):
    pass
