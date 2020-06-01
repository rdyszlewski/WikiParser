from parser.common.models import Meaning, Relation, Translation


class ParseResult:

    def __init__(self, number=None):
        self.number = number


class MeaningSetter:

    @staticmethod
    def set_meanings_result(results_list: list, meanings: dict):
        for result in results_list:
            meaning = Meaning()
            meaning.part_of_speech = result.pos
            meaning.gender = result.gender
            meaning.registers = result.registers
            meaning.definition = result.definition
            meaning.link = result.link

            meanings[result.number] = meaning

    @staticmethod
    def set_examples_result(results_list: list, meanings: dict):
        for result in results_list:
            number = result.number
            if number in meanings:
                meaning = meanings[number]
                example = MeaningSetter._create_text_from_list_elements(result)
                meaning.examples.append(example)

    @staticmethod
    def _create_text_from_list_elements(result):
        return ' '.join(result.elements)

    @staticmethod
    def set_relations_result(results_list: list, meanings: dict, relation_type):
        for result in results_list:
            number = result.number
            if number in meanings:
                meaning = meanings[number]
                words = MeaningSetter._remove_commas_from_relation_elements(result)
                relation = Relation(relation_type, words)
                meaning.relations.append(relation)

    @staticmethod
    def _remove_commas_from_relation_elements(relation_elements):
        return [word.replace(',', '') for word in relation_elements.elements]

    @staticmethod
    def set_translations_result(results_list: list, meanings: dict):
        for result in results_list:
            number = result.number
            if number in meanings:
                meaning = meanings[number]
                translation = Translation(result.language, result.translations)
