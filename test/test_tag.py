from unittest import TestCase

from container.tag import Tag


class TestTag(TestCase):
    def setUp(self):
        self.tag = Tag(['SyncManager', 'SyncConfig', 'SyncFactory'])

    def test_get_files_count_should_return_three(self):
        actual = self.tag.get_files_count()
        expected = 3
        self.assertEqual(expected, actual)

    def test_add_file_should_add_one_file(self):
        self.tag.add_file('SyncFoo')
        actual = self.tag.files
        expected = ['SyncManager', 'SyncConfig', 'SyncFactory', 'SyncFoo']
        self.assertEqual(expected, actual)
