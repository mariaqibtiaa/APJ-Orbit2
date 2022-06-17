import json
import os
import numpy as np
from major.common import split_and_clean_words
from major.major_info_csv import get_all_major_info_from_csv
from major.major_info_preprocess import process_orginal_major_info


# all unique word list, sorted
all_words = []

# key: word, value: index in all_words
all_words_idx = {}

# key: major name, value: description and major name word list
all_majors = {}

# key: major name, value: tf_idf value vector
all_majors_tf_idf = {}

# key: major name, value: dict: key: word, value: tf_idf value in the major description
all_majors_word_tf_idf = {}

major_info_json_filename = 'major_info_json.txt'

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, 'data')

major_info_json_filepath = os.path.join(data_path, major_info_json_filename)


# return a set of words
def get_words_set(ison_input):
    word_set = set()
    for major, words in ison_input.items():
        major_words = split_and_clean_words(major)
        all_majors[major] = words + major_words
        for word in all_majors[major]:
            word_set.add(word)
    return word_set


def get_all_majors_from_json():
    f = open(major_info_json_filepath, "r")
    tmp = f.readline()
    tmp = json.loads(tmp)
    word_set = get_words_set(tmp)
    global all_words
    all_words = sorted(list(word_set))
    for idx, word in enumerate(all_words):
        all_words_idx[word] = idx


def get_idf_count(word):
    cnt = 0
    for _, words in all_majors.items():
        if word in words:
            cnt += 1
    return cnt


def process_tf_idf(major):
    count = {}
    for word in all_majors[major]:
        count[word] = count[word]+1 if word in count else 1

    tf_idf_vec = np.zeros([len(all_words), 1])
    all_majors_word_tf_idf[major] = {}

    for word in all_majors[major]:
        tf = count[word]
        N = len(all_majors)
        idf_count = get_idf_count(word)
        idf = np.log2(N*1.0 / idf_count)
        tf_idf = tf * idf
        tf_idf_vec[all_words_idx[word]] = tf_idf
        all_majors_word_tf_idf[major][word] = tf_idf

    # process words in major
    # max_tf_idf = max(tf_idf_vec)
    # for word in split_and_clean_words(major):
    #     idx = all_words_idx[word]
    #     tf_idf = 0.5 * max_tf_idf
    #     tf_idf_vec[idx] = tf_idf
    #     all_majors_word_tf_idf[major][word] = tf_idf

    all_majors_tf_idf[major] = tf_idf_vec
    # print(major, all_majors_word_tf_idf[major])


def process_all_major_tf_idf():
    process_orginal_major_info()
    get_all_majors_from_json()
    get_all_major_info_from_csv()
    for major, _ in all_majors.items():
        process_tf_idf(major)

    test_tf_idf_value()


def test_tf_idf_value():
    for major, _ in all_majors.items():
        for word, val in all_majors_word_tf_idf[major].items():
            idx = all_words_idx[word]
            if all_majors_tf_idf[major][idx] != val:
                print('Error: {0} in major {1} has problem'.format(word, major))


if __name__ == '__main__':
    process_all_major_tf_idf()
