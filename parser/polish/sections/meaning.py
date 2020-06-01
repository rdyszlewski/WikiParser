import regex as re

from parser.polish.result import ParseResult
from parser.polish.sections.common import ParserHelper
from parser.polish.values import Values

DEFINITION_PATTERN = 'definition'
LINK_PATTERN = 'link'
REGISTER_PATTERN = 'register'
NUMBER_PATTERN = 'number'


class MeaningParser:

    def __init__(self, patterns, symbols):
        self._patterns = patterns
        self._symbols = symbols

    def parse(self, section_text: str, title: str) -> list:
        meanings_result = []
        current_pos = None
        current_gender = None
        for line in section_text.splitlines():
            if self._is_pos_and_gender_line(line):
                current_gender, current_pos = self._get_gender_and_pos(section_text)
            elif self._is_definition_line(line):
                number, definition, registers, link = self._get_meaning(line, title)
                result = MeaningResult(number, current_pos, current_gender, registers, definition, link)

                meanings_result.append(result)
        return meanings_result

    def _is_pos_and_gender_line(self, line):
        return line.startswith("''")

    def _is_definition_line(self, line):
        return line.startswith(":")

    def _get_gender_and_pos(self, text: str):
        line_text = self._get_post_and_gender_part(text)
        gender = Values.get_gender(line_text, self._symbols)
        pos = Values.get_part_of_speech(line_text, self._symbols)
        return gender, pos

    def _get_post_and_gender_part(self, text):
        line_text = text.strip().split('\n', 1)[0]
        line_text = line_text.replace("''", "")
        return line_text

    def _get_meaning(self, text: str, title: str):
        registers = self._get_registers(text)
        number = ParserHelper.get_number(text, self._patterns['number'])
        definition = self._get_definition(text)
        link = self._get_link(text)
        if link == '':
            link = title
        return number, definition, registers, link

    def _get_definition(self, text):
        definition_pattern = self._patterns[DEFINITION_PATTERN]
        definition_match = re.finditer(definition_pattern, text)
        definition_elements = []
        for match in definition_match:
            definition_part = match.group(1)
            definition_part = ParserHelper.get_text_part(definition_part)
            if match.group(2):
                part_ending = match.group(2).replace(']]', '')
                definition_part = definition_part + part_ending
            definition_elements.append(definition_part)
        definition = ' '.join(definition_elements)
        return definition

    def _get_registers(self, text):
        register_pattern = self._patterns[REGISTER_PATTERN]
        register_match = re.findall(register_pattern, text)
        registers_elements = []
        for register in register_match:
            if self._is_correct_register(register):
                registers_elements.append(register)
        return registers_elements

    def _is_correct_register(self, register):
        return register != 'wikipedia' \
               and '|' not in register

    def _get_link(self, text: str):
        link_pattern = self._patterns[LINK_PATTERN]
        link_match = re.search(link_pattern, text)
        if link_match:
            link = link_match.group(1)
            if link != '':
                link_bytes = bytes(link, 'utf-8')
                link_result = link_bytes.decode('utf-8')
                return link_result
        return None


class MeaningResult(ParseResult):

    def __init__(self, number=None, pos=None, gender=None, registers=None, definition=None, link=None):
        super().__init__(number)
        self.pos = pos
        self.gender = gender
        if not registers:
            registers = []
        self.registers = registers
        self.definition = definition
        self.link = link
