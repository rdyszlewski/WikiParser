import regex as re

from parser.common.models import Relation
from parser.english.connector import MeaningConnector
from parser.english.sections.common import ParserHelper
from parser.english.values import Values

SPECIAL_RELATIONS_PATTERN = 'special_relations'
RELATIONS_PATTERN = 'relations'
RELATION_MEANING_PATTERN = 'relation_meaning'


class RelationsParser:

    def __init__(self, patterns, symbols):
        self.__patterns = patterns
        self.__symbols = symbols
        self.__relation_map = Values.get_relations_map(self.__symbols)
        self.__meaning_connector = MeaningConnector()

    def parse(self, lines, index, parser_result):
        line = lines[index]
        relation_type_text = self.__get_relation_type_from_header(line)
        relations_list, index = self.__parse_relations(lines, index + 1, relation_type_text)
        self.__meaning_connector.connect_relations_to_meanings(parser_result, relations_list)
        return index

    @staticmethod
    def __get_relation_type_from_header(line):
        relation_type_text = line[4:-4]
        return relation_type_text

    def __parse_relations(self, lines, start_index, relation_text):
        relation_type = self.__get_relation_type_from_text(relation_text)
        current_line = ''
        index = start_index - 1
        lines_length = len(lines)
        relation_result = []
        while ParserHelper.is_end_of_section(current_line, index, lines_length):
            index += 1
            current_line = lines[index]
            if self.__is_relation_line(current_line):
                self.__serve_relations_line(current_line, relation_type, relation_result)
        return relation_result, index

    def __serve_relations_line(self, current_line, relation_type, relation_result):
        relation_meaning = self.__get_relation_meaning(current_line)
        words = self.__get_relations(current_line)
        relation = RelationResult(relation_type, words, relation_meaning)
        relation_result.append(relation)

    def __get_relation_type_from_text(self, relation_type_text):
        assert relation_type_text in self.__relation_map
        return self.__relation_map[relation_type_text]

    def __is_relation_line(self, line):
        return line.startswith(self.__patterns['relation_line'])

    def __get_relation_meaning(self, text):
        relation_meaning_pattern = self.__patterns[RELATION_MEANING_PATTERN]
        # relation_meaning_pattern = '\* {{sense\|(.*?)}}'
        relation_meaning_match = re.search(relation_meaning_pattern, text)
        if relation_meaning_match:
            relation_meaning = relation_meaning_match.group(1)
            return relation_meaning

    def __get_relations(self, text):
        relations_pattern = self.__patterns[RELATIONS_PATTERN]
        relations_match = re.findall(relations_pattern, text)
        if relations_match:
            relations_result = [relation for relation in relations_match]
            return relations_result
        else:
            relations_result = self.__get_special_relations(text)
            return relations_result

    def __get_special_relations(self, text):
        special_relations_pattern = self.__patterns[SPECIAL_RELATIONS_PATTERN]
        relations_match = re.findall(special_relations_pattern, text)
        return relations_match


class RelationResult(Relation):

    def __init__(self, type=None, words=None, meaning=''):
        super().__init__(type, words)
        self.meaning = meaning
