from parser.common.values import Languages, Gender, PartOfSpeech, RelationTypes
from parser.polish.symbols import PolishSymbols


class Values:

    @staticmethod
    def get_relations_map(symbols: PolishSymbols):
        relations_map = {symbols.synonyms: RelationTypes.SYNONYMS, symbols.antonyms: RelationTypes.ANTONYMS,
                         symbols.hyponyms: RelationTypes.HYPONYMS,
                         symbols.hypernyms: RelationTypes.HYPERNYMS, symbols.holonyms: RelationTypes.HOLONYMS,
                         symbols.meronyms: RelationTypes.MERONYMS}
        return relations_map

    @staticmethod
    def get_language_map(symbols: PolishSymbols):
        language_map = {symbols.english: Languages.ENGLISH, symbols.spanish: Languages.SPANISH}
        return language_map

    @staticmethod
    def get_languages_section_map(symbols: PolishSymbols):
        languages_section_map = {Languages.POLISH: symbols.polish_section, Languages.ENGLISH: symbols.english_section}
        return languages_section_map

    @staticmethod
    def get_language_from_section(language_text, symbols: PolishSymbols):
        if language_text == symbols.polish_section:
            return Languages.POLISH
        elif language_text == symbols.english_section:
            return Languages.ENGLISH

    @staticmethod
    def get_gender(text, symbols: PolishSymbols):
        if symbols.musculine in text:
            gender = Gender.MUSCULINE
        elif symbols.feminine in text:
            gender = Gender.FEMININE
        elif symbols.neutral in text:
            gender = Gender.NEUTRAL
        else:
            gender = Gender.LACK
        return gender

    @staticmethod
    def get_part_of_speech(text, symbols: PolishSymbols):
        if symbols.noun in text:
            pos = PartOfSpeech.NOUN
        elif symbols.verb in text:
            pos = PartOfSpeech.VERB
        elif symbols.adjective in text:
            pos = PartOfSpeech.ADJECTIVE
        elif symbols.adverb in text:
            pos = PartOfSpeech.ADVERB
        else:
            pos = PartOfSpeech.LACK
        return pos
