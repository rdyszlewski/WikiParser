from nltk import word_tokenize, pos_tag
from textblob import TextBlob

from interwiktionary_mapper.analyzer.analyzer import Analyzer
from interwiktionary_mapper.analyzer.pos import PartOfSpeech


class EnglishAnalyzer(Analyzer):

    def analyse(self, sentence):
        tagged_words = self.__get_tagged_words(sentence)
        result = []
        for i, element in enumerate(tagged_words):
            word = element[0]
            word_blob = TextBlob(word)
            if len(word_blob.words) > 0:
                word = word_blob.words[0].singularize()
            tag = element[1]
            pos = self._get_pos(tag)
            result.append((word, pos))
        return result

    def get_base_words(self, sentence):
        tagged_words = self.__get_tagged_words(sentence)
        base_words = [element[0] for element in tagged_words]
        return base_words

    @staticmethod
    def __get_tagged_words(sentence):
        tokens = word_tokenize(sentence)
        tagged_words = pos_tag(tokens)
        return tagged_words

    @staticmethod
    def _get_pos(tag):
        pos_map = {'v': PartOfSpeech.VERB,
                   'n': PartOfSpeech.NOUN,
                   'j': PartOfSpeech.ADJECTIVE,
                   'r': PartOfSpeech.ADVERB}
        tag = tag[0].lower()
        if tag in pos_map:
            return pos_map[tag]
        return None
