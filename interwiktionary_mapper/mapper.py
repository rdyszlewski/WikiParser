import pickle

from interwiktionary_mapper.analyzer.analyzer import Analyzer
from interwiktionary_mapper.analyzer.english import EnglishAnalyzer
from interwiktionary_mapper.dictionary import Dictionary
from interwiktionary_mapper.models import MappingMeaning
from parser.common.models import Meaning


class InterWiktionaryMapper:
    """" Rzutowanie wpisów pochodzących z różnych wersji językowych Wiktionary, ale pochodzących z tego samego języka
    (np. angielskie wpisy z polskiej Wiktionary i angielskie wpisy z angielskiej wersji Wiktionary)
    W polskiej wersji definicje w innych językach są zapisane jako tłumaczenia w języku polskim. Dlatego potrzebny jest
    słownik polsko angielski. """

    def __init__(self):
        self.__analyzer = EnglishAnalyzer()

    def start(self, source_wiki_path: str, target_wiki_path: str, dictionary: Dictionary):
        source_wiki = self._load_parser_result(source_wiki_path)
        target_wiki = self._load_parser_result(target_wiki_path)

        result_map = {}
        for word, source_meanings in source_wiki.items():
            target_meanings = self._find_meanings_by_word(word, target_wiki)
            for index, meaning in enumerate(source_meanings):
                best_index, best_meaning = self.__find_most_matching(meaning, target_meanings, dictionary)
                if meaning and best_meaning:
                    mapping_meaning = self._get_mapping_meaning(meaning, word, index)
                    best_mapping_meaning = self._get_mapping_meaning(best_meaning, word, best_index)
                    result_map[mapping_meaning] = best_mapping_meaning
        return result_map

    def __find_most_matching(self, source_meaning, target_meaning, dictionary):
        best_score = 0
        best_meaning = None
        best_index = -1
        for second_index, second_meaning in enumerate(target_meaning):
            score = self._score_meanings_similarity(source_meaning, second_meaning, dictionary)
            if score > best_score:
                best_score = score
                best_meaning = second_meaning
                best_index = second_index
        return best_index, best_meaning

    @staticmethod
    def _get_mapping_meaning(meaning, word, index):
        definition = meaning.definition
        pos = meaning.part_of_speech
        mapping_meaning = MappingMeaning(word, pos, index, meaning, definition)
        return mapping_meaning

    @staticmethod
    def _load_parser_result(path):
        return pickle.load(open(path, 'rb'))

    @staticmethod
    def _find_meanings_by_word(word, wiki):
        if word in wiki:
            return wiki[word]
        return []

    def _score_meanings_similarity(self, first_meaning: Meaning, second_meaning: Meaning, dictionary: Dictionary):
        translation_score = self._score_translation_similarity(first_meaning, second_meaning)
        relation_score = self._score_relations_similarity(first_meaning, second_meaning)
        definition_score = self._score_definition_similarity(first_meaning, second_meaning, dictionary)

        return translation_score + relation_score + definition_score

    def _score_definition_similarity(self, first_meaning: Meaning, second_meaning: Meaning, dictionary: Dictionary):
        first_meanings_parts = first_meaning.definition.split(',')
        definition_translations = []
        for part in first_meanings_parts:
            translations = dictionary.get_translations(part)
            definition_translations.extend(translations)
        second_meaning_definition = second_meaning.definition
        definition_elements = self.__analyzer.analyse(second_meaning_definition)
        definition_words = [element[Analyzer.WORD] for element in definition_elements]
        common_words = set(definition_translations).intersection(set(definition_words))

        return len(common_words)

    @staticmethod
    def _score_translation_similarity(first_meaning: Meaning, second_meaning: Meaning):
        score = 0
        translations = first_meaning.definition.split(',')
        for translation in translations:
            for second_translation in second_meaning.translations:
                for translation_word in second_translation.translations:
                    if translation == translation_word:
                        score += 1
        return score

    def _score_relations_similarity(self, first_meaning: Meaning, second_meaning: Meaning):
        score = 0
        for first_relation in first_meaning.relations:
            for second_relation in second_meaning.relations:
                if first_relation.type == second_relation.type:
                    common_elements = self._count_common_elements(first_relation.words, second_relation.words)
                    if common_elements > 0:
                        print()
                    score += common_elements
        return score

    @staticmethod
    def _count_common_elements(first_list, second_list):
        first = set(first_list)
        second = set(second_list)
        common = first.intersection(second)
        return len(common)

    @staticmethod
    def _get_translation_from_langauge(translations, language):
        return [translation for translation in translations if translation.language == language]
