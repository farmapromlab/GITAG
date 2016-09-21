import os
import shutil

from pyh import *

css_path = '/gitag/report/css'
logo_path = '/gitag/report/logo'
report_path = '/gitag/report/'
class_report_path = '/gitag/report/classes/'


# Html report generator -------------------------


def generate_tag_report(project_path, sorted_tags_map, deleted_files, none_tagged_files, branch_1, branch_2):
    if not os.path.exists(project_path + css_path):
        os.makedirs(project_path + css_path)
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/css/base-style.css', project_path + css_path)
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/css/style.css', project_path + css_path)
    if not os.path.exists(project_path + logo_path):
        os.makedirs(project_path + logo_path)
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/logo/gitag_logo.svg', project_path + logo_path)

    page = PyH('GITAG Summary')
    page.addCSS('css/base-style.css')
    page.addCSS('css/style.css')

    content = page << div(id='content')
    content << h1('GITAG Summary')
    content << h2('Difference between ' + branch_1 + ' and ' + branch_2)
    content << h2('')

    div_table = content << div(id='table', cl='tab')
    content_table = div_table << table()
    content_table_head = content_table << tr()
    content_table_head << th('Tag name')
    content_table_head << th('Count')

    for tag in sorted_tags_map:
        content_table_body = content_table << tr()
        key = content_table_body << td(cl='tag')
        link = 'classes/' + tag[0] + '.html'
        key << a(tag[0], href=link)
        content_table_body << td(tag[1].get_files_count())
        generate_class_report(project_path, branch_1, branch_2, tag[0], tag[1].files)

    if deleted_files.__len__() != 0:
        link = 'classes/DELETED_FILES.html'
        content << h2('')
        content << a('DELETED_FILES', href=link, id='footer')
        generate_deleted_class_report(project_path, branch_1, branch_2, 'DELETED_FILES', deleted_files)

    if none_tagged_files.__len__() != 0:
        link = 'classes/UNTAGGED_FILES.html'
        content << h2('')
        content << a('UNTAGGED_FILES', href=link, id='footer')
        generate_deleted_class_report(project_path, branch_1, branch_2, 'UNTAGGED_FILES', none_tagged_files)

    content << div(id='footer') << img(src='logo/gitag_logo.svg', height="50")

    if not os.path.exists(project_path + report_path):
        os.makedirs(project_path + report_path)
    gitag_output_path = project_path + report_path + 'index.html'
    page.printOut(gitag_output_path)


def generate_class_report(project_path, branch_1, branch_2, tag, files):
    page = PyH('GITAG Summary')
    page.addCSS('../css/base-style.css')
    page.addCSS('../css/style.css')

    content = page << div(id='content')
    content << h1(tag)
    content << h2('Difference between ' + branch_1 + ' and ' + branch_2)
    content << h2('')

    div_table = content << div(id='table', cl='tab')
    content_table = div_table << table()
    content_table_head = content_table << tr()
    content_table_head << th('File name')
    content_table_head << th('Added lines [%]')
    content_table_head << th('Deleted lines [%]')
    content_table_head << th('Status')
    content_table_head << th('Kind')

    for file in files:
        content_table_body = content_table << tr()
        key = content_table_body << td(cl='class')
        key << a(file.file_path.split('/')[-1])
        content_table_body << td(file.get_added_files_percent())
        content_table_body << td(file.get_deleted_files_percent())
        content_table_body << td(file.get_status())
        content_table_body << td('class')

        if file.test_file is not None:
            content_table_body = content_table << tr()
            key = content_table_body << td(cl='test')
            key << a(file.test_file.file_path.split('/')[-1])
            content_table_body << td(file.test_file.get_added_files_percent())
            content_table_body << td(file.test_file.get_deleted_files_percent())
            content_table_body << td(file.test_file.get_status())
            content_table_body << td('test')

    content << div(id='footer') << img(src='../logo/gitag_logo.svg', height="50")

    if not os.path.exists(project_path + class_report_path):
        os.makedirs(project_path + class_report_path)
    gitag_output_path = project_path + class_report_path + tag + '.html'
    page.printOut(gitag_output_path)


def generate_deleted_class_report(project_path, branch_1, branch_2, tag, files):
    page = PyH('GITAG Summary')
    page.addCSS('../css/base-style.css')
    page.addCSS('../css/style.css')

    content = page << div(id='content')
    content << h1(tag)
    content << h2('Difference between ' + branch_1 + ' and ' + branch_2)
    content << h2('')

    div_table = content << div(id='table', cl='tab')
    content_table = div_table << table()
    content_table_head = content_table << tr()
    content_table_head << th('File name')

    for file in files:
        content_table_body = content_table << tr()
        key = content_table_body << td(cl='success')
        key << a(file.file_path.split('/')[-1])

    content << div(id='footer') << img(src='../logo/gitag_logo.svg', height="50")

    if not os.path.exists(project_path + class_report_path):
        os.makedirs(project_path + class_report_path)
    gitag_output_path = project_path + class_report_path + tag + '.html'
    page.printOut(gitag_output_path)
