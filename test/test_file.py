from unittest import TestCase
import mmap
import os

from container.file import File


class TestFile(TestCase):
    def test_get_added_files_percent_should_return_correct_value(self):
        f = File('/foo/File', None, 20, 5)
        f.lines = 200
        actual = f.get_added_files_percent()
        expected = 10.0
        self.assertEqual(expected, actual)

    def test_get_added_files_percent_should_return_zero_for_empty_file(self):
        actual = File('/foo/File', None, 20, 5).get_added_files_percent()
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_deleted_files_percent_should_return_correct_value(self):
        f = File('/foo/File', None, 20, 5)
        f.lines = 200
        actual = f.get_deleted_files_percent()
        expected = 2.5
        self.assertEqual(expected, actual)

    def test_get_deleted_files_percent_should_return_zero_for_empty_file(self):
        actual = File('/foo/File', None, 20, 5).get_deleted_files_percent()
        expected = 0
        self.assertEqual(expected, actual)

    def test_get_status_should_return_added_state(self):
        f = File('/foo/File', None, 200, 5)
        f.lines = 200
        actual = f.get_status()
        expected = 'Added'
        self.assertEqual(expected, actual)

    def test_get_status_should_return_modified_state(self):
        f = File('/foo/File', None, 123, 5)
        f.lines = 200
        actual = f.get_status()
        expected = 'Modified'
        self.assertEqual(expected, actual)

    # File should be mocked but I could not find any way to mock fileno() in mock_file :(( Mby in python 3+
    def test_get_file_lines_should_return_four_lines_for_file_with_last_empty_line(self):
        path = os.path.dirname(os.path.abspath(
            __file__)) + '/data/test_get_file_lines_should_return_four_lines_for_file_with_last_empty_line'
        f = open(path)
        file_content = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        f = File('/foo/File', file_content, 1, 1)
        actual = f.lines
        expected = 4
        file_content.close()
        self.assertEqual(expected, actual)

    # File should be mocked but I could not find any way to mock fileno() in mock_file :(( Mby in python 3+
    def test_get_file_lines_should_return_four_lines_for_file_without_last_empty_line(self):
        path = os.path.dirname(os.path.abspath(
            __file__)) + '/data/test_get_file_lines_should_return_four_lines_for_file_without_last_empty_line'
        f = open(path)
        file_content = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        f = File('/foo/File', file_content, 1, 1)
        actual = f.lines
        expected = 4
        file_content.close()
        self.assertEqual(expected, actual)

    def test_get_file_lines_should_return_zero_for_empty_file(self):
        f = File('/foo/File', None, 20, 5)
        actual = f.lines
        expected = 0
        self.assertEqual(expected, actual)
