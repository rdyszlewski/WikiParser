import regex as re

from parser.common.values import Languages
from parser.english.values import Values

LANGUAGE_PATTERN = 'language'


class LanguageParser:

    def __init__(self, patterns, symbols):
        self.__patterns = patterns
        self.__symbols = symbols
        self.__language_map = Values.get_language_map(self.__symbols)

    def parse(self, lines, index):
        line = lines[index]
        language_text = self.__get_language_from_header(line)
        language = self.__get_language(language_text)
        if not self.__is_parser_language(language):
            index = self.__find_next_language_section_index(lines, index + 1)
            if index < len(lines):
                return language, index
        return language, index + 1

    @staticmethod
    def __get_language_from_header(line):
        language_text = line[2:-2]
        return language_text

    def __get_language(self, language_text):
        if language_text in self.__language_map:
            return self.__language_map[language_text]

    # TODO: dodać obsługę z konfiguracji. W angielskie Wiktionary powinna być możliwość wyszukiwania w róznych językach
    @staticmethod
    def __is_parser_language(language):
        return language == Languages.ENGLISH

    def __find_next_language_section_index(self, lines, start_index):
        language_pattern = self.__patterns[LANGUAGE_PATTERN]
        current_index = start_index
        while current_index < len(lines):
            line = lines[current_index]
            if re.match(language_pattern, line):
                return current_index
            current_index += 1
        return len(lines)
