from unittest import TestCase

from container.file import File
from container.tag import Tag
from controller import files_controller
from controller.files_controller import FilesController


class TestFilesController(TestCase):
    def setUp(self):
        self.regex = '@Tag\(([^\)]+)\)'
        self.extension = 'java'
        self.divider = ','
        self.start = '@Tag('
        self.end = ')'
        self.ignore = ['{', '}']
        self.language = {"regex": self.regex,
                         "extension": self.extension,
                         "divider": self.divider,
                         "start": self.start,
                         "end": self.end,
                         "ignore": self.ignore}

    def test_parse__should_return_just_deleted_files(self):
        controller = FilesController('',
                                     [File('name.java', None, 20, 4), File('name2.java', None, 3, 1)],
                                     self.language)
        controller.parse(is_file_exists_false, get_tags_from_file_not_empty)

        self.assertEqual(2, controller.deleted_files.__len__())

    def test_parse__should_return_just_none_tagged_files(self):
        controller = FilesController('',
                                     [File('name.java', None, 20, 4), File('name2.java', None, 3, 1)],
                                     self.language)
        controller.parse(is_file_exists_true, get_tags_from_file_empty)

        self.assertEqual(2, controller.none_tagged_files.__len__())

    def test_parse__should_return_just_java_none_tagged_file(self):
        java_file = File('name.java', None, 20, 4)
        controller = FilesController('', [java_file, File('name2.kt', None, 3, 1)], self.language)
        controller.parse(is_file_exists_true, get_tags_from_file_empty)

        self.assertEqual([java_file], controller.none_tagged_files)

    def test_parse__should_return_just_tagged_files(self):
        controller = FilesController('',
                                     [File('name.java', None, 20, 4), File('name2.java', None, 3, 1)],
                                     self.language)
        controller.parse(is_file_exists_true, get_tags_from_file_not_empty)

        self.assertEqual(2, controller.tags.items().__len__())

    def test_parse__should_return_just_java_tagged_file(self):
        java_file = File('name.java', None, 20, 4)
        controller = FilesController('', [java_file, File('name2.kt', None, 3, 1)], self.language)
        controller.parse(is_file_exists_true, get_tags_from_file_not_empty)

        self.assertEqual([java_file], controller.tags.values()[0].files)
        self.assertEqual([java_file], controller.tags.values()[1].files)

    def test_parse__should_return_just_test_files(self):
        files = [File('HelloWorldTest.java', None, 20, 4), File('HelloWorld.java', None, 3, 1)]
        controller = FilesController('', files, self.language)
        controller.parse(is_file_exists_true, get_tags_from_file_not_empty)

        self.assertEqual(1, controller.test_files.__len__())

    def test_sort_tags__should_desc_sort_by_tags_count(self):
        controller = FilesController('',
                                     [File('name.java', None, 20, 4), File('name2.java', None, 3, 1)],
                                     self.language)
        controller.tags = {'TAG_1': Tag([File]), 'TAG_2': Tag([File, File, File])}
        sorted_tags = files_controller.sort(controller.tags, True)

        self.assertEqual('TAG_2', sorted_tags[0][0])
        self.assertEqual('TAG_1', sorted_tags[1][0])

    def test_sort_tags__should_sort_by_tags_count(self):
        controller = FilesController('',
                                     [File('name.java', None, 20, 4), File('name2.java', None, 3, 1)],
                                     self.language)
        controller.tags = {'TAG_1': Tag([File]), 'TAG_2': Tag([File, File, File])}
        sorted_tags = files_controller.sort(controller.tags, False)

        self.assertEqual('TAG_1', sorted_tags[0][0])
        self.assertEqual('TAG_2', sorted_tags[1][0])

    def test_put_tags_to_map__should_put_three_tags_to_map(self):
        actual = {}
        tags = ['TAG_1',
                'TAG_2',
                'TAG_3'
                ]
        files_controller.put_tags_to_map(actual, tags, File('', None, 5, 5))

        self.assertEquals(1, actual['TAG_1'].get_files_count())
        self.assertEquals(1, actual['TAG_2'].get_files_count())
        self.assertEquals(1, actual['TAG_3'].get_files_count())

    def test_put_tags_to_map__should_increment_values_for_keys(self):
        actual = {'TAG_1': Tag(['file']),
                  'TAG_2': Tag(['file']),
                  'TAG_3': Tag(['file'])
                  }
        tags = ['TAG_1',
                'TAG_2',
                'TAG_3'
                ]
        files_controller.put_tags_to_map(actual, tags, File('', None, 5, 5))

        self.assertEquals(2, actual['TAG_1'].get_files_count())
        self.assertEquals(2, actual['TAG_2'].get_files_count())
        self.assertEquals(2, actual['TAG_3'].get_files_count())

    def test_get_tags_from_file__should_return_empty_list(self):
        actual = files_controller.get_tags_from_file("Foo foo foo",
                                                     self.regex,
                                                     self.start,
                                                     self.end,
                                                     self.divider,
                                                     self.ignore)

        self.assertEquals(0, actual.__len__())

    def test_get_tags_from_file__should_return_one_tag_for_annotation_with_one_element(self):
        actual = files_controller.get_tags_from_file("Foo foo @Tag(TAG) foo",
                                                     self.regex,
                                                     self.start,
                                                     self.end,
                                                     self.divider,
                                                     self.ignore)
        expected = ['TAG']

        self.assertEquals(expected, actual)

    def test_get_tags_from_file__should_return_one_tag_for_annotation_with_array_with_one_element(self):
        actual = files_controller.get_tags_from_file("Foo foo @Tag({TAG}) foo",
                                                     self.regex,
                                                     self.start,
                                                     self.end,
                                                     self.divider,
                                                     self.ignore)
        expected = ['TAG']

        self.assertEquals(expected, actual)

    def test_get_tags_from_file__should_return_many_tags(self):
        actual = files_controller.get_tags_from_file("Foo foo @Tag({TAG_1, TAG_2, TAG_3}) foo",
                                                     self.regex,
                                                     self.start,
                                                     self.end,
                                                     self.divider,
                                                     self.ignore)
        expected = ['TAG_1',
                    'TAG_2',
                    'TAG_3'
                    ]

        self.assertEquals(expected, actual)

    def test_get_tags_from_file__should_return_many_tags_for_multi_line_tag_declaration(self):
        actual = files_controller.get_tags_from_file("Foo foo @Tag({TAG_1, TAG_2, TAG_3}) "
                                                     "public void main()",
                                                     self.regex,
                                                     self.start,
                                                     self.end,
                                                     self.divider,
                                                     self.ignore)
        expected = ['TAG_1',
                    'TAG_2',
                    'TAG_3'
                    ]

        self.assertEquals(expected, actual)

    def test_add_test_files_to_files_in_tags__should_pair_correctly(self):
        tags = {'TAG_1': Tag([
            File('MedicalSampleSeriesQuantitySpentPerMedicalClientForProducer.java', None, 0, 0),
            File('MedicalSampleSeriesQuantitySpentPerMedicalClientForProducerOnObjectParsed.kt', None, 0, 0),
        ])}
        test_files = [
            File('MedicalSampleSeriesQuantitySpentPerMedicalClientForProducerOnObjectParsedTest.groovy', None, 0, 0),
            File('HelloWorldTest.java', None, 0, 0)
        ]

        files_controller.match_test_files_to_files_in_tags(tags, test_files)

        files = tags['TAG_1'].files

        self.assertEqual(None, files[0].test_file)
        self.assertEqual('MedicalSampleSeriesQuantitySpentPerMedicalClientForProducerOnObjectParsedTest.groovy',
                         files[1].test_file.file_path)

    def test_add_tags_to_existing_map__should_insert_new_tag(self):
        # GIVEN
        new_tag_key = 'TAG_3'
        new_tag_value = Tag([File('new_file1.java', None, 0, 0)])
        # AND
        new_tags = {new_tag_key: new_tag_value}
        existing_tags = {}

        # WHEN
        files_controller.add_tags_to_existing_map(existing_tags, new_tags)

        # THEN
        self.assertEqual(new_tag_value, existing_tags.get(new_tag_key))

    def test_add_tags_to_existing_map__should_add_file_to_existing_tag(self):
        # GIVEN
        existing_tag_key = 'TAG_1'
        new_tag_value = Tag([File('new_file1.java', None, 0, 0)])
        # AND
        new_tags = {existing_tag_key: new_tag_value}
        existing_tags = {
            existing_tag_key: Tag([
                File('file1.java', None, 0, 0),
                File('file2.java', None, 0, 0),
            ])
        }

        # WHEN
        files_controller.add_tags_to_existing_map(existing_tags, new_tags)

        # THEN
        self.assertEqual(new_tag_value.files[0], existing_tags.get(existing_tag_key).files[-1])
        self.assertEqual(3, existing_tags.get(existing_tag_key).get_files_count())

    def test_add_tags_to_existing_map__should_not_add_same_file_to_existing_tag(self):
        # GIVEN
        existing_tag_key = 'TAG_1'
        existing_tag = Tag([File('file1.java', None, 0, 0)])
        # AND
        new_tags = {existing_tag_key: existing_tag}
        existing_tags = {existing_tag_key: Tag([File('file1.java', None, 0, 0)])}

        # WHEN
        files_controller.add_tags_to_existing_map(existing_tags, new_tags)

        # THEN
        self.assertEqual(existing_tag, existing_tags.get(existing_tag_key))
        self.assertEqual(1, existing_tags.get(existing_tag_key).get_files_count())


# noinspection PyUnusedLocal
def is_file_exists_true(system_file_path):
    return True


# noinspection PyUnusedLocal
def is_file_exists_false(system_file_path):
    return False


# noinspection PyUnusedLocal
def get_tags_from_file_empty(file_content, regex, start, end, divider, ignore):
    return []


# noinspection PyUnusedLocal
def get_tags_from_file_not_empty(file_content, regex, start, end, divider, ignore):
    return ['Tag1', 'Tag2']
