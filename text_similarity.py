from nltk import word_tokenize
import numpy as np
from simhash import Simhash


def cos_similarity(_a: str, _b: str):
    """
    Cosine similarity between two strings.
    Use nltk.word_tokenize to do segmentation,
    and then calculate the cosine similarity.

    ** It is recommended for short texts. **

    :param _a: one string
    :param _b: the other string
    :return: cosine similarity
    """
    words_a = word_tokenize(_a)
    words_b = word_tokenize(_b)
    word_set = set(_a + _b)
    a_cnt = np.array([words_a.count(each) for each in word_set])
    b_cnt = np.array([words_b.count(each) for each in word_set])
    if (np.linalg.norm(a_cnt) * np.linalg.norm(b_cnt)) == 0:
        return 0
    else:
        return np.sum(a_cnt * b_cnt) / (np.linalg.norm(a_cnt) * np.linalg.norm(b_cnt))


def simhash_similarity(_a: str, _b: str):
    """
    Simhash similarity(Google) between two strings.
    Use pkg<simhash> to calculate hamming distance directly,
    then calculate their similarity.

    ** It is recommended for long texts. **

    :param _a: one string
    :param _b: the other string
    :return: simhash similarity
    """
    s1 = Simhash(_a)
    s2 = Simhash(_b)
    dist = s1.distance(s2)
    return 1 - dist / 64


if __name__ == '__main__':
    a = "A group of kids is playing in a yard and an old man is standing in the background"
    b = "A group of boys in a yard is playing and a man is standing in the background"
    print(cos_similarity(a, b))
    print(simhash_similarity(a, b))
