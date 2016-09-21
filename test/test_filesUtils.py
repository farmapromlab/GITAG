from unittest import TestCase

from util import file_utils


class TestFilesUtils(TestCase):
    def test_get_system_file_path_should_return_correct_system_file_path(self):
        project_path = '/Users/user'
        file_path = 'ProjectName/HelloWorld.java'

        actual = file_utils.get_system_file_path(project_path, file_path)
        expected = '/Users/user/ProjectName/HelloWorld.java'

        self.assertEqual(expected, actual)
