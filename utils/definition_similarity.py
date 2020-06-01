class DefinitionSimilarity:

    @staticmethod
    def get_definition_similarity_score(definition1: str, definition2: str):
        definition1_text = definition1.replace(',', '')
        definition2_text = definition2.replace(',', '')
        definition1_array = definition1_text.split(' ')
        definition2_array = definition2_text.split(' ')
        common_elements = list(set(definition1_array).intersection(definition2_array))
        return len(common_elements)
