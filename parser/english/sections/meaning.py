import regex as re

from parser.common.models import Meaning
from parser.english.sections.common import ParserHelper
from parser.english.values import Values

DEFINITION_PATTERN = 'definition'
EXAMPLE_PATTERN = 'example'
REGISTER_PATTERN = 'register'


class MeaningParser:

    def __init__(self, patterns, symbols):
        self.__patterns = patterns
        self.__symbols = symbols
        self.__pos_map = Values.get_pos_map(self.__symbols)

    def parse(self, lines, index, title):
        if ParserHelper.is_special_title(title):
            return [], index + 1
        meanings_list, index = self._parse_meanings(lines, index)
        return meanings_list, index

    def _parse_meanings(self, lines, start_index):
        line = lines[start_index]
        pos = self.__get_part_of_speech(line)
        assert pos is not None, lines[start_index]
        index = start_index
        current_line = ''
        current_meaning = None
        meanings_result = []
        lines_length = len(lines)
        while ParserHelper.is_end_of_section(current_line, index, lines_length):
            index += 1
            current_line = lines[index]
            if self.__is_definition_line(current_line):
                current_meaning = self.__serve_definition_line(current_line, pos, meanings_result, current_meaning)
            elif self.__is_example_line(current_line):
                self.__serve_example_line(current_line, current_meaning)
        if self.__added_new_meaning(current_meaning):
            meanings_result.append(current_meaning)
        return meanings_result, index

    @staticmethod
    def __added_new_meaning(meaning: Meaning):
        return meaning is not None

    def __serve_example_line(self, current_line, current_meaning):
        example = self.__get_example(current_line)
        if example and current_meaning:
            current_meaning.examples.append(example)

    def __serve_definition_line(self, current_line, pos, meanings_result, current_meaning):
        registers = self.__get_registers(current_line)
        definition = self._get_definition(current_line)
        if current_meaning:
            meanings_result.append(current_meaning)
        current_meaning = Meaning(pos, definition)
        current_meaning.registers = registers
        return current_meaning

    def __get_part_of_speech(self, text):
        text = text.rstrip()
        pos = text[3:-3]
        if pos in self.__pos_map:
            return self.__pos_map[pos]

    def __is_definition_line(self, line):
        return line.startswith(self.__patterns['definition_line'])

    def __is_example_line(self, line):
        return line.startswith(self.__patterns['example_line'])

    def __get_registers(self, text):
        register_pattern = self.__patterns[REGISTER_PATTERN]
        registers_match = re.search(register_pattern, text)
        if registers_match:
            registers_text = registers_match.group(1)
            registers = registers_text.split('|')
            return registers
        return []

    def _get_definition(self, text):
        definition_pattern = self.__patterns[DEFINITION_PATTERN]
        definition_match = re.match(definition_pattern, text)
        if definition_match:
            definition = definition_match.group(2)
            definition = self.__get_text_part(definition)
            definition = self.__clean_definition(definition)
            return definition

    @staticmethod
    def __get_text_part(group_text):
        if '|' in group_text:
            parts = group_text.split('|')
            text_part = parts[1]
        else:
            text_part = group_text
        return text_part

    @staticmethod
    def __clean_definition(definition: str) -> str:
        result_definition = definition
        if '}}' in result_definition:
            result_definition = result_definition[result_definition.index('}}') + 3:]
        result_definition = result_definition.replace('[[', '').replace(']]', '')
        return result_definition

    def __get_example(self, text):
        example_pattern = self.__patterns[EXAMPLE_PATTERN]
        example_match = re.match(example_pattern, text)
        if example_match:
            example = example_match.group(1)
            example = self.__clean_example(example)
            return example

    def __clean_example(self, example):
        example = example.replace("'''", "")
        return example
