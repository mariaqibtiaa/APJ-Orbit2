import numpy as np
from operator import itemgetter
from major.tf_idf import process_all_major_tf_idf, all_majors_word_tf_idf
from major.major_info_csv import major_info_dict
from major.major_info_preprocess import major_name_mapping, major_info_original
from major import common

TOP_K = 5


def alloc_weight_to_words(n, start=10, end=10):
    if n <= 3:
        return np.linspace(start, start, n)
    return np.linspace(start, end, n)


# return the top_k (major_name, rating), input: user input string.
def cal_user_input_rating(user_input):
    words = common.split_and_clean_words(user_input)
    words_weight = alloc_weight_to_words(len(words))
    major_rating = list()
    for major, tfidf_dict in all_majors_word_tf_idf.items():
        total_rating = 0.0
        for word, weight in zip(words, words_weight):
            if word in tfidf_dict:
                total_rating += tfidf_dict[word] * weight
        major_rating.append((major, total_rating))
    major_rating.sort(key=itemgetter(1), reverse=True)
    return major_rating


def filter_result(pre_results, category=None, income_threshold=0):
    if len(pre_results) <= TOP_K:
        return pre_results

    filtered = []
    while len(filtered) < TOP_K:
        filtered.clear()
        for result in pre_results:
            if result[0] not in major_info_dict:
                continue
            match = 0
            if (category is None) or (major_info_dict[result[0]]['category'] == category):
                match += 1
            if major_info_dict[result[0]]['income'] >= income_threshold:
                match += 1
            if match == 2:
                filtered.append(result)
            if len(filtered) >= TOP_K:
                return filtered

        if len(filtered) >= TOP_K:
            return filtered

        if category is not None:
            category = None
            continue

        income_threshold -= 5000

    return filtered


def test_algorithm():
    s1 = 'I like mathematics and physics a lot, want to do engineering works.'
    s2 = 'I like teaching.'
    s3 = 'I like reading naval and like writing stories and articles.'
    s4 = 'I like animals a lot and want to be a researcher in biology and medical.'
    S = [s1, s2, s3, s4]
    while True:
        idx = 0 # int(input("Input the index: "))
        res = cal_user_input_rating(S[idx])
        # res = filter_result(res, category='Engineering', income_threshold=30000)
        res = filter_result(res, income_threshold=500)
        # print(S[idx])
        # print(res)
        for tmp in res:
            name = tmp[0]
            name = major_name_mapping[name]
            info = major_info_original[name]
            print('{0}, rating: {1}, category: {2}, income: {3}:\n{4}\n***********'
                  .format(name, tmp[1], major_info_dict[tmp[0]]['category'], major_info_dict[tmp[0]]['income'], info))
        break


if __name__ == '__main__':
    # all init
    process_all_major_tf_idf()
    print('shit')
    test_algorithm()

