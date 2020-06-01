from parser.polish.symbols import PolishSymbols


class Settings:

    @staticmethod
    def get_relations(symbols: PolishSymbols):
        relations = [symbols.synonyms, symbols.antonyms, symbols.hypernyms, symbols.hyponyms, symbols.holonyms,
                     symbols.meronyms]
        return relations
