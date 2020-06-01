import yaml

from parser.common.values import Sections
from configuration.configuration import Configuration
from parser.english.sections.language import LanguageParser
from parser.english.sections.meaning import MeaningParser
from parser.english.sections.relations import RelationsParser
from parser.english.sections.translations import TranslationsParser
from parser.english.symbols import EnglishSymbols
from parser.english.values import Values

LANGUAGE_SECTION = 'language_section'
MEANING_SECTION = 'meaning_section'
INFO_SECTION = 'info_section'


class EnglishWiktionaryParser:

    def __init__(self, configuration):
        self.__symbols = None
        self.__patterns = None
        self.__configuration = self.__load_settings(configuration)
        self.__relations_map = Values.get_relations_map(self.__symbols)
        self.__language_map = Values.get_language_map(self.__symbols)
        self.__pos_map = Values.get_pos_map(self.__symbols)

    def __load_settings(self, configuration:Configuration):
        self.__symbols = EnglishSymbols(configuration.get_symbols_path())
        pattern_file = open(configuration.get_patterns_path())
        self.__patterns = yaml.safe_load(pattern_file)
        pattern_file.close()
        return configuration

    def parse_text(self, text: str, title=None, parser_result=None):
        assert text is not None

        current_line_index = 0
        result = []
        lines = text.splitlines()
        language_parser = LanguageParser(self.__patterns, self.__symbols)
        meaning_parser = MeaningParser(self.__patterns, self.__symbols)
        relations_parser = RelationsParser(self.__patterns, self.__symbols)
        translations_parser = TranslationsParser(self.__patterns, self.__symbols)
        while current_line_index < len(lines):
            line = lines[current_line_index].strip()
            if not self._is_section_line(line):  # not section
                current_line_index += 1
                continue
            section = self._get_section(line)
            if section == Sections.LANGUAGE:
                _, current_line_index = language_parser.parse(lines, current_line_index)
            elif section == Sections.MEANINGS:
                meanings, current_line_index = meaning_parser.parse(lines, current_line_index, title)
                result.extend(meanings)
            elif section == Sections.RELATIONS:
                current_line_index = relations_parser.parse(lines, current_line_index, result)
            elif section == Sections.TRANSLATIONS:
                current_line_index = translations_parser.parse(lines, current_line_index + 1, title, parser_result,
                                                               result)
            else:
                current_line_index += 1
            if current_line_index == None:
                print()
        return result

    @staticmethod
    def _is_section_line(line):
        return line.startswith('=')

    def _get_section(self, text: str):
        info = self.__patterns[INFO_SECTION]
        meaning = self.__patterns[MEANING_SECTION]
        language = self.__patterns[LANGUAGE_SECTION]
        if text.startswith(info):
            section_title = self._get_relation_type_from_header(text)
            if section_title in self.__relations_map:
                return Sections.RELATIONS
            if section_title == self.__symbols.translations:
                return Sections.TRANSLATIONS
        elif text.startswith(meaning):
            section_title = text[3:-3]
            if section_title in self.__pos_map:
                return Sections.MEANINGS
        elif text.startswith(language):
            return Sections.LANGUAGE
        return Sections.NOT_SUPPORTED

    @staticmethod
    def _get_relation_type_from_header(line):
        relation_type_text = line[4:-4]
        return relation_type_text
