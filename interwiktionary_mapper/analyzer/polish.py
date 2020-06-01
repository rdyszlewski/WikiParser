import morfeusz2

from interwiktionary_mapper.analyzer.analyzer import Analyzer
from interwiktionary_mapper.analyzer.pos import PartOfSpeech
from interwiktionary_mapper.analyzer.tags import Tags


class PolishAnalyzer(Analyzer):

    def __init__(self):
        self._analyzer = morfeusz2.Morfeusz()

    def analyse(self, sentence):
        result_list = []
        analyse_result = self._analyzer.analyse(sentence)
        for result in analyse_result:
            word = self._get_base_form_from_analyse_result(result)
            pos = self._get_pos_from_analyse_result(result)
            result_list.append((word, pos))
        return result_list

    @staticmethod
    def _get_base_form_from_analyse_result(analyse_result):
        return analyse_result[2][1].split(':')[0]

    def get_base_words(self, sentence):
        analyze_result = self._analyzer.analyse(sentence)
        return [self._get_base_form_from_analyse_result(result) for result in analyze_result]

    def _get_pos_from_analyse_result(self, analyse_result):
        text = analyse_result[2][2].split(':')[0]
        return self._get_part_of_speech_by_tag(text)

    @staticmethod
    def _get_part_of_speech_by_tag(tag):
        if tag in Tags.NOUN_TAGS:
            return PartOfSpeech.NOUN
        if tag in Tags.VERB_TAGS:
            return PartOfSpeech.VERB
        if tag in Tags.ADJECTIVE_TAGS:
            return PartOfSpeech.ADJECTIVE
        if tag in Tags.ADVERBS_TAG:
            return PartOfSpeech.ADVERB
        return None
