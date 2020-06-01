from parser.common.values import PartOfSpeech, Languages, RelationTypes
from parser.english.symbols import EnglishSymbols


class Values:

    @staticmethod
    def get_pos_map(symbols: EnglishSymbols):
        pos_map = {symbols.noun: PartOfSpeech.NOUN,
                   symbols.verb: PartOfSpeech.VERB,
                   symbols.adverb: PartOfSpeech.ADVERB,
                   symbols.adjective: PartOfSpeech.ADJECTIVE}
        return pos_map

    @staticmethod
    def get_language_map(symbols: EnglishSymbols):
        language_map = {symbols.polish: Languages.POLISH,
                        symbols.english: Languages.ENGLISH,
                        symbols.spanish: Languages.SPANISH}
        return language_map

    @staticmethod
    def get_relations_map(symbols: EnglishSymbols):
        relations_map = {symbols.synonyms: RelationTypes.SYNONYMS,
                         symbols.hypernyms: RelationTypes.HYPERNYMS,
                         symbols.hyponyms: RelationTypes.HYPONYMS}
        return relations_map
