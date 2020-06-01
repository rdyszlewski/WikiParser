import regex as re
import yaml

from configuration.configuration import Configuration
from parser.polish.result import MeaningSetter
from parser.polish.sections.example import ExampleParser
from parser.polish.sections.meaning import MeaningParser
from parser.polish.sections.relations import RelationsParser
from parser.polish.sections.translations import TranslationParser
from parser.polish.settings import Settings
from parser.polish.symbols import PolishSymbols
from parser.polish.values import Values

LANGUAGE_PATTERN = 'language'


class PolishWiktionaryParser():

    def __init__(self, configuration: Configuration):
        self._current_meaning = None
        self.__symbols = None
        self.__patterns = None
        self.__configuration = self.__load_settings(configuration)
        self.__relations_map = Values.get_relations_map(self.__symbols)
        self.__language_map = Values.get_language_map(self.__symbols)
        self.__languages_section_map = Values.get_languages_section_map(self.__symbols)
        self.__relations = Settings.get_relations(self.__symbols)

    def __load_settings(self, configuration: Configuration):
        self.__symbols = PolishSymbols(configuration.get_symbols_path())
        pattern_file = open(configuration.get_patterns_path())
        self.__patterns = yaml.safe_load(pattern_file)
        pattern_file.close()
        return configuration

    def parse_text(self, text: str, title: str = None, parser_result: list = None):
        assert text
        start_index, language = self._get_language_section_start_index(text, self.__languages_section_map[
            self.__configuration.get_language()])
        if start_index < 0:
            return None
        lines = text[start_index + 1:].splitlines()
        section_text = ''
        last_section = None
        meanings = {}
        meanings_parser = MeaningParser(self.__patterns, self.__symbols)
        examples_parser = ExampleParser(self.__patterns, self.__symbols)
        relations_parser = RelationsParser(self.__patterns, self.__symbols)
        translations_parser = TranslationParser(self.__patterns, self.__symbols, self.__language_map)
        for index, line in enumerate(lines):
            line = line.strip()
            if line.startswith(self.__symbols.start_section):
                if PolishWiktionaryParser.__is_meaning_section(last_section, self.__symbols):
                    meaning_results = meanings_parser.parse(section_text, title)
                    MeaningSetter.set_meanings_result(meaning_results, meanings)
                elif PolishWiktionaryParser.__is_examples_section(last_section, self.__symbols):
                    examples_result = examples_parser.parse(section_text)
                    MeaningSetter.set_examples_result(examples_result, meanings)
                elif self.__is_relations_section(last_section):
                    relations_result = relations_parser.parse(section_text)
                    MeaningSetter.set_relations_result(relations_result, meanings, self.__relations_map[last_section])
                elif PolishWiktionaryParser.__is_translations_section(last_section, self.__symbols):
                    translation_result = translations_parser.parse(section_text)
                    MeaningSetter.set_translations_result(translation_result, meanings)
                section_text = ''
                last_section = line
            elif line.startswith(self.__symbols.start_language_section):
                return PolishWiktionaryParser.__create_result_list_from_map(meanings)
            else:
                section_text += line + '\n'
        return PolishWiktionaryParser.__create_result_list_from_map(meanings)

    @staticmethod
    def __is_meaning_section(section, symbols: PolishSymbols):
        return section == symbols.meanings

    @staticmethod
    def __is_examples_section(section, symbols: PolishSymbols):
        return section == symbols.examples

    def __is_relations_section(self, section):
        return section in self.__relations

    @staticmethod
    def __is_translations_section(section, symbols: PolishSymbols):
        return section == symbols.translations

    @staticmethod
    def __create_result_list_from_map(result_map):
        return [value for key, value in result_map.items()]

    @staticmethod
    def __is_empty_text_element(text_element):
        return text_element == '' or text_element == ',' or text_element.isspace()

    def _get_language_section_start_index(self, text, allowable_language, start_search_index=0):
        assert text
        assert start_search_index >= 0
        current_index = start_search_index
        while current_index > -1:
            current_index, language = self._match_language_section(text, current_index)
            if language == allowable_language:
                language_code = Values.get_language_from_section(language, self.__symbols)
                return current_index, language_code
        return -1, ''

    def _match_language_section(self, text, current_index):
        language_pattern = self.__patterns[LANGUAGE_PATTERN]
        language_match = re.search(language_pattern, text, pos=current_index)
        if language_match:
            language = language_match.group(1)
            index = language_match.end()
            return index, language
        return -1, ''
