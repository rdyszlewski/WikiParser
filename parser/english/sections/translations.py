import regex as re

from parser.common.models import Translation
from parser.english.connector import MeaningConnector
from parser.english.sections.common import ParserHelper
from parser.english.values import Values

MEANING_TRANSLATION_PATTERN = 'meaning_translation'
TRANSLATION_PATTERN = 'translation'
TRANSLATION_LANGUAGE_PATTERN = 'translation_language'


class TranslationsParser:

    def __init__(self, patterns, symbols):
        self.__patterns = patterns
        self.__symbols = symbols
        self.__languages_map = Values.get_language_map(self.__symbols)
        self.__meaning_connector = MeaningConnector()

    def parse(self, lines, index, title, parser_result, result):
        translations_list, index = self.__parse_translations(lines, index)
        meanings = self.__get_meanings(title, result, parser_result)
        self.__meaning_connector.connect_translations_to_meanings(meanings, translations_list)
        return index

    def __get_meanings(self, title, result, parser_result):
        if ParserHelper.is_special_title(title):
            word = title.split('/')[0]
            meanings = parser_result[word] if word in parser_result else []
        else:
            meanings = result
        return meanings

    def __parse_translations(self, lines, start_index):
        current_line = ''
        index = start_index - 1
        lines_length = len(lines)
        translations_result = []
        current_meaning = None
        while ParserHelper.is_end_of_section(current_line, index, lines_length):
            index += 1
            current_line = lines[index]
            if self.__is_translation_line(current_line):
                self.__serve_translations_line(current_line, current_meaning, translations_result)
            elif self.__is_start_meaning_translation(current_line):
                current_meaning = self.__get_meaning_translation(current_line)
        return translations_result, index

    def __serve_translations_line(self, current_line, current_meaning, translations_result):
        language = self.__get_translations_language(current_line)
        if language:
            translations = self.__get_translations(current_line)
            translation = TranslationResult(language, translations, current_meaning)
            translations_result.append(translation)

    def __is_translation_line(self, line):
        return line.startswith(self.__patterns['translation_line'])

    def __get_translations_language(self, text):
        language_pattern = self.__patterns[TRANSLATION_LANGUAGE_PATTERN]
        language_match = re.match(language_pattern, text)
        if language_match:
            language_text = language_match.group(1)
            language = self.__get_language(language_text)
            return language

    def __is_support_language(self, language):
        return language in self.__languages_map

    def __get_language(self, language_text):
        if language_text in self.__languages_map:
            return self.__languages_map[language_text]

    def __get_translations(self, text):
        translation_pattern = self.__patterns[TRANSLATION_PATTERN]
        translation_match = re.finditer(translation_pattern, text)
        assert translation_match
        translations_result = [translation.group(1) for translation in translation_match]
        return translations_result

    @staticmethod
    def __is_start_meaning_translation(line):
        return line.startswith('{{trans-top|')

    def __get_meaning_translation(self, line):
        translation_meaning_pattern = self.__patterns[MEANING_TRANSLATION_PATTERN]
        match = re.search(translation_meaning_pattern, line)
        if match:
            return match.group(1)


class TranslationResult(Translation):

    def __init__(self, language=None, translations=None, meaning=''):
        super().__init__(language, translations)
        self.meaning = meaning
