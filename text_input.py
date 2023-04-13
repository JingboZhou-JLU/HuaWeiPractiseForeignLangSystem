import re
import string

import spacy


class Text:
    def __init__(self, path):
        self._path = path
        with open(path, 'r', encoding='utf-8') as fp:
            text = fp.read()
        self._text = text
        self._as_sentence = self.__split_as_sentence()
        self._as_word = self.__split_as_word()

    def __split_as_sentence(self):
        sentences = re.split(r'(\.|\!|\?|。|！|？|\.{6})', self._text)
        ret = list(filter(lambda x: x not in string.punctuation, sentences))
        ret = list(map(lambda x: x.strip(), ret))
        return ret

    def __split_as_word(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self._text)
        ret = list(map(str, list(doc)))
        ret = list(map(lambda x: x.strip(), ret))
        return list(filter(lambda x: x not in string.punctuation + '“”', ret))

    @property
    def sentences(self):
        return self._as_sentence

    @property
    def words(self):
        return self._as_word


if __name__ == '__main__':
    text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
    obj = Text(text)
    print(obj.sentences)
    print(obj.words)

