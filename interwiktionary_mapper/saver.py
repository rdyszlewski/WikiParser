import json

from parser.common.file_helper import JsonSaver


class MappingSaver:

    @staticmethod
    def save_to_file(path, mapping_result):
        result = {}
        for meaning, mapping in mapping_result.items():
            meaning_json = JsonSaver.create_meaning_map(meaning.meaning)

            key = MappingSaver._create_meaning_key(meaning.word, meaning.position, meaning.pos, meaning.definition)
            value = meaning_json
            result[key] = value

        with open(path, 'w') as file:
            file.write(json.dumps(result))

    @staticmethod
    def _create_meaning_key(word, position, pos, definition):
        key = '{} :{} :{} :{}'.format(word, position, pos, definition)
        return key
