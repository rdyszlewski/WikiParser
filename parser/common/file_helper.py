import json

from parser.common.models import Meaning
from parser.common.models import Relation, Translation

DEFINITION = 'definition'
PART_OF_SPEECH = 'part_of_speech'
GENDER = 'gender'
EXAMPLES = 'examples'
REGISTERS = 'registers'
RELATIONS = 'relations'
TRANSLATIONS = 'translations'
LINK = 'link'


class JsonSaver:

    @staticmethod
    def save_to_json(result, path):
        map_result = {}
        for word, meanings in result.items():
            meanings_list = []
            for meaning in meanings:
                meaning_result = JsonSaver.create_meaning_map(meaning)
                meanings_list.append(meaning_result)
            if word is not None:
                map_result[word] = meanings_list

        with open(path, 'w') as file:
            file.write(json.dumps(map_result))

    @staticmethod
    def create_meaning_map(meaning):
        meaning_result = {}
        if meaning.definition is not None:
            meaning_result[DEFINITION] = meaning.definition
        if meaning.part_of_speech is not None:
            meaning_result[PART_OF_SPEECH] = meaning.part_of_speech
        if meaning.gender is not None:
            meaning_result[GENDER] = meaning.gender
        if meaning.examples:
            meaning_result[EXAMPLES] = meaning.examples
        if meaning.registers:
            meaning_result[REGISTERS] = meaning.registers
        if meaning.relations:
            meaning_result[RELATIONS] = JsonSaver._create_relations(meaning.relations)
        if meaning.translations:
            meaning_result[TRANSLATIONS] = JsonSaver._create_translations(meaning.translations)
        if meaning.link:
            meaning_result[LINK] = meaning.link
        return meaning_result

    @staticmethod
    def _create_relations(relations):
        result = {}
        for relation in relations:
            type = relation.type
            if type is not None:
                result[type] = relation.words
        return result

    @staticmethod
    def _create_translations(translations):
        result = {}
        for translation in translations:
            language = translation.language
            if language is not None:
                result[language] = translation.translations
        return result

    @staticmethod
    def read_from_json(path):
        result = {}
        with open(path, 'r') as file:
            meanings_map = json.load(file)
            for word, meanings in meanings_map.items():
                meaning_list = []
                for meaning_entry in meanings:
                    meaning = Meaning()
                    if DEFINITION in meaning_entry:
                        meaning.definition = meaning_entry[DEFINITION]
                    if PART_OF_SPEECH in meaning_entry:
                        meaning.part_of_speech = meaning_entry[PART_OF_SPEECH]
                    if GENDER in meaning_entry:
                        meaning.gender = meaning_entry[GENDER]
                    if EXAMPLES in meaning_entry:
                        meaning.examples = meaning_entry[EXAMPLES]
                    if REGISTERS in meaning_entry:
                        meaning.registers = meaning_entry[REGISTERS]
                    if RELATIONS in meaning_entry:
                        meaning.relations = JsonSaver._get_relations_from_map(meaning_entry[RELATIONS])
                    if TRANSLATIONS in meaning_entry:
                        meaning.translations = JsonSaver._get_translations_from_map(meaning_entry[TRANSLATIONS])
                    if LINK in meaning_entry:
                        meaning.link = meaning_entry[LINK]
                    meaning_list.append(meaning)
                result[word] = meaning_list
        return result

    @staticmethod
    def _get_relations_from_map(relations_map):
        relations_result = []
        for type, words in relations_map.items():
            relation = Relation(type, words)
            relations_result.append(relation)
        return relations_result

    @staticmethod
    def _get_translations_from_map(translations_map):
        translations_result = []
        for language, translations in translations_map.items():
            translation = Translation(language, translations)
            translations_result.append(translation)
        return translations_result
