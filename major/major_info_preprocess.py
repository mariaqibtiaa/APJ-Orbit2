import re
import json
import os
from major.common import split_and_clean_words

# key: major name, value: description word list.
major_info_dict = {}

# key: original major name, value: string of original description.
major_info_original = {}

# key: processed major name, value: original major name.
major_name_mapping = {}

major_original_info_filename = 'major_original_info.txt'
major_info_json_filename = 'major_info_json.txt'

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')

major_original_info_filepath = os.path.join(data_path, major_original_info_filename)
major_info_json_filepath = os.path.join(data_path, major_info_json_filename)


def read_original_info():
    f = open(major_original_info_filepath, 'r')
    lines = f.readlines()
    lines = list(map(lambda x: x.rstrip(), lines))
    lines = list(filter(lambda x: len(x) > 0, lines))
    return lines


def read_and_clean_original_info():
    f = open(major_original_info_filepath, 'r')
    lines = f.readlines()
    lines = list(map(lambda x: x.rstrip(), lines))
    lines = list(filter(lambda x: len(x) > 0, lines))
    lines = list(map(lambda x: x.lower(), lines))
    lines = list(map(lambda x: re.sub(r'[^\w\s]','',x) if not x.startswith('****') else x, lines))
    return lines


def get_major_info_dict(lines, info_dict):
    # lines = read_and_clean_original_info()
    read_title = False
    read_info = False
    tmp = {}
    for line in lines:
        if line.startswith('***'):
            read_title = True
            read_info = False
            if 'title' in tmp:
                info_dict[tmp['title']] = tmp['des']
        elif read_title:
            tmp['title'] = line
            tmp['des'] = ''
            read_info = True
            read_title = False
        elif read_info:
            tmp['des'] = tmp['des'] + ' ' + line


def get_major_name_mapping():
    for name in major_info_original.keys():
        tmp = name.lower()
        tmp = re.sub(r'[^\w\s]', '', tmp)
        major_name_mapping[tmp] = name


def refactor_major_info_dict():
    for key, val in major_info_dict.items():
        major_info_dict[key] = split_and_clean_words(val)
        # print(key)
        # print(major_info_dict[key])

    res = json.dumps(major_info_dict)
    f = open(major_info_json_filepath, 'w')
    f.write(res)
    f.close()


def process_orginal_major_info():
    get_major_info_dict(read_and_clean_original_info(), major_info_dict)
    get_major_info_dict(read_original_info(), major_info_original)
    get_major_name_mapping()
    refactor_major_info_dict()


if __name__ == '__main__':
    process_orginal_major_info()
    print(major_info_dict)
    print(major_info_original)
    print(major_name_mapping)
