import re

EXCLUDED_WORDS = [
    'a', 'all', 'also', 'an', 'and', 'any', 'are', 'as',
    'at', 'be', 'but', 'by', 'for', 'from', 'in', 'is',
    'it', 'its', 'may', 'of', 'on', 'or', 'other', 'out',
    'such', 'that', 'the', 'this', 'to', 'with', 'i',
]


# return list of non-plural word
def process_word_suffix(word):
    if word.endswith('ing'):
        return [re.sub('ing$', '', word)]
    if word.endswith('ies'):
        return [re.sub('ies$', 'y', word), re.sub('ies$', 'ie', word)]
    if word.endswith('es'):
        return [re.sub('es$', '', word), re.sub('es$', 'e', word)]
    if word.endswith('s'):
        return [re.sub('s$', '', word)]
    return []


# split a string, changes words to lowercase, delete non important characters and words.
def split_and_clean_words(input_str):
    words = input_str.split()
    words = list(map(lambda x: x.rstrip(), words))
    words = list(map(lambda x: x.lower(), words))
    words = list(map(lambda x: re.sub(r'[^\w\s]', '', x), words))
    words = list(filter(lambda x: len(x) > 0 and (x not in EXCLUDED_WORDS), words))
    res = words
    for word in words:
        res += process_word_suffix(word)
    return res


if __name__ == '__main__':
    tmp = sorted(EXCLUDED_WORDS)
    print(tmp)