from parser.common.models import Translation, Relation, Meaning


class MeaningConnector:

    def connect_translations_to_meanings(self, meanings, translations):
        connection_result = self.__get_meanings_connection_map(meanings, translations)
        for definition, meaning in connection_result.items():
            if meaning:
                filtered_translations = self._filter_elements_by_definition(definition, translations)
                translations_list = self.__get_translations_from_result(filtered_translations)
                meaning.translations = translations_list

    def connect_relations_to_meanings(self, meanings, relations):
        connection_result = self.__get_meanings_connection_map(meanings, relations)
        for relation_definition, meaning in connection_result.items():
            if meaning:
                filtered_relations = self._filter_elements_by_definition(relation_definition, relations)
                relations_list = self.__get_relations_from_result(filtered_relations)
                meaning.relations.extend(relations_list)

    @staticmethod
    def __get_translations_from_result(translation_result):
        return [Translation(result.language, result.translations) for result in translation_result]

    @staticmethod
    def __get_relations_from_result(relations_result):
        return [Relation(result.type, result.words) for result in relations_result]

    @staticmethod
    def _filter_elements_by_definition(definition, elements):
        return [element for element in elements if element.meaning == definition]

    def __get_meanings_connection_map(self, meanings, elements):
        used_unit = {}
        connection_result = {}

        elements_definitions = self.__get_unique_definitions(elements)
        for definition in elements_definitions:
            best_meaning = self.__find_best_translation_fit(definition, meanings, used_unit)
            connection_result[definition] = best_meaning
        return connection_result

    @staticmethod
    def __get_unique_definitions(elements):
        elements_meanings = set([element.meaning for element in elements if element.meaning is not None])
        return elements_meanings

    @staticmethod
    def __get_meaning_definitions(meanings):
        meaning_definitions = set([meaning.definition for meaning in meanings])
        return meaning_definitions

    @staticmethod
    def __create_translations_definitions_map(translations):
        translation_definitions_map = {}
        for index, translation in enumerate(translations):
            meaning = translation.meaning
            if meaning is None:
                continue
            if meaning not in translation_definitions_map:
                translation_definitions_map[meaning] = []
            translation_definitions_map[meaning].append(index)
        return translation_definitions_map

    def __find_best_translation_fit(self, element_definition, meanings, used_definitions):
        best_meaning: Meaning = None
        best_similarity = 0
        for meaning in meanings:
            if element_definition in used_definitions:
                continue
            similarity_score = self.__get_definition_similarity_score(element_definition, meaning.definition)
            if similarity_score > best_similarity:
                best_similarity = similarity_score
                best_meaning = meaning
        return best_meaning

    @staticmethod
    def __get_definition_similarity_score(definition1: str, definition2: str):
        definition1_text = definition1.replace(',', '').lower()
        definition2_text = definition2.replace(',', '').lower()
        definition1_array = definition1_text.split(' ')
        definition2_array = definition2_text.split(' ')
        common_elements = list(set(definition1_array).intersection(definition2_array))
        return len(common_elements)

    def __create_translations_map(self, indices, translations):
        translations_elements = [translations[index] for index in indices]
        translations_map = self.__get_translations_map(translations_elements)
        return translations_map

    @staticmethod
    def __get_translations_by_indices(translations_result, indices):
        translations = []
        for index in indices:
            translation_result = translations_result[index]
            translation = Translation(translation_result.language, translation_result.translations)
            translations.append(translation)
        return translations

    @staticmethod
    def __get_relations_by_indices(relations_result, indices):
        relations = []
        for index in indices:
            relation_result = relations_result[index]
            relation = Relation(relation_result.type, relation_result.words)
            relations.append(relation)
        return relations

    @staticmethod
    def __get_element_by_indices(elements, indices):
        return [elements[i] for i in indices]

    @staticmethod
    def __get_translations_map(translations):
        translations_result = {}
        for translation in translations:
            translations_result[translation.language] = translation.translations
        return translations_result
