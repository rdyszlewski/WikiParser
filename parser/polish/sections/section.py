import regex as re

from parser.polish.result import ParseResult
from parser.polish.sections.common import ParserHelper

NUMBER_PATTERN = 'number'
EXAMPLE_PATTERN = 'example'


class SectionParser:

    def __init__(self, patterns, symbols):
        self._patterns = patterns
        self._symbols = symbols

    def _parse_section(self, section_text):
        section_result = []
        for line in section_text.splitlines():
            line = line.rstrip()
            number, parse_result = self._parse_line(line)
            result = ElementResult(number, parse_result)
            section_result.append(result)

        return section_result

    def _parse_line(self, line):
        number, parse_elements = self._parse_meaning_text(line)
        return number, parse_elements

    def _parse_meaning_text(self, line):
        number = ParserHelper.get_number(line, self._patterns[NUMBER_PATTERN])
        text_elements = self._get_text_elements(line)
        return number, text_elements

    def _get_text_elements(self, line, with_coma=True):
        pattern = self._patterns[EXAMPLE_PATTERN]
        text_parts = []
        text_match = re.findall(pattern, line)
        for group in text_match:
            group_text = group[0]
            if self.__is_empty_text_element(group_text):
                continue
            text_part = ParserHelper.get_text_part(group_text)
            text_part = self._clean_text(group_text, text_part, with_coma)
            if not text_part.isspace():
                text_parts.append(text_part)
        return text_parts

    @staticmethod
    def _clean_text(group_text, text_part, with_coma):
        if ']]' in group_text:
            text_part = text_part.replace(']]', '')
        if not with_coma and ',' in text_part:
            text_part = text_part.replace(',', '')
        return text_part

    @staticmethod
    def __is_empty_text_element(text_element):
        return text_element == '' or text_element == ',' or text_element.isspace()


class ElementResult(ParseResult):

    def __init__(self, number=None, elements=None):
        super().__init__(number)
        if elements is None:
            elements = []
        self.elements = elements
