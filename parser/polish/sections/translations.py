from parser.polish.result import ParseResult
from parser.polish.sections.section import SectionParser

NUMBER_PATTERN = 'number'


class TranslationParser(SectionParser):

    def __init__(self, patterns, symbols, language_map):
        super().__init__(patterns, symbols)
        self.__language_map = language_map

    def parse(self, section_text):
        if section_text.startswith(self._symbols.translations):
            return []
        return self._parse_translation_section(section_text)

    def _parse_translation_section(self, section_text):
        section_result = []
        for line in section_text.splitlines():
            line = line.rstrip()
            language_text, translations_text = self._split_line_on_language_and_translations(line)
            language = self._get_language(language_text)
            if language:
                translations_results = self._parse_translations(language, translations_text)
                section_result.extend(translations_results)
        return section_result

    def _get_language(self, language_text):
        if language_text in self.__language_map:
            return self.__language_map[language_text]
        return None

    def _split_line_on_language_and_translations(self, line):
        if self._is_translation_line(line):
            start_lang_index = line.index('*')
            if ':' not in line:  # TODO: poprawić to
                return '', ''
            end_lang_index = line.index(':')
            language_text = line[start_lang_index + 2: end_lang_index]
            translations_text = line[end_lang_index + 1:]
            return language_text, translations_text
        return '', ''

    def _is_translation_line(self, line):
        if len(line) == 0:
            return False
        return line[0] == '*'

    def _parse_translations(self, language, translation_line):
        section_result = []
        translations = translation_line.split(';')
        for translation in translations:
            number, parse_result = self._parse_line(translation)
            result = TranslationResult(number, language, parse_result)

            section_result.append(result)
        return section_result


class TranslationResult(ParseResult):

    def __init__(self, number=None, language=None, translations=None):
        super().__init__(number)
        self.language = language
        self.translations = translations
        if translations is None:
            self.translations = []
