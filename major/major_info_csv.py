import csv
import os

# csv file name
csv_filename = "data/all_ages.csv"

# field list
fields = []

# row data
rows = []

# key: category name, value: major name list
category_to_major = {}

# key: major name, the mapped name from description table,
# value: info dict with 'cat', 'income', and 'other_name'
major_info_dict = {}

# key: name in the major info table, value: name in the major description table
major_name_mapping = {}


major_name_filename = 'major_name.txt'
category_name_filename = 'category_name.txt'
all_ages_filename = 'all_ages.csv'

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')

major_name_filepath = os.path.join(data_path, major_name_filename)
category_name_filepath = os.path.join(data_path, category_name_filename)
all_ages_filepath = os.path.join(data_path, all_ages_filename)


def read_cvs_data():
    global fields
    with open(all_ages_filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = True
        for row in csvreader:
            if first_row:
                fields = row
                first_row = False
            else:
                rows.append(row)


def get_major_category():
    for row in rows:
        # category = row[2].lower()
        category = row[2]
        major = row[1].lower()
        if major in major_name_mapping:
            tmp = major
            major = major_name_mapping[major]
            major_info_dict[major] = {}
            major_info_dict[major]['category'] = category
            major_info_dict[major]['income'] = float(row[-3])
            major_info_dict[major]['other_name'] = tmp
            if category in category_to_major:
                category_to_major[category].append(major)
            else:
                category_to_major[category] = [major]


def get_major_name_mapping():
    f = open(major_name_filepath, 'r')
    lines = f.readlines()
    for line in lines:
        tmp = line.split(',')
        name_a = tmp[0]
        name_b = tmp[1].strip()
        major_name_mapping[name_a] = name_b


def save_category_names():
    f = open(category_name_filepath, 'w')
    for name in category_to_major.keys():
        f.write(name + '\n')


def get_all_major_info_from_csv():
    get_major_name_mapping()
    read_cvs_data()
    get_major_category()
    save_category_names()
    # print(major_info)
    # print(category_to_major)


if __name__ == "__main__":
    get_all_major_info_from_csv()
