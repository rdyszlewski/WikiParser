import abc


class IParser:
    GENDER = 'gender'
    POS = 'pos'
    REGISTER = 'register'
    MEANINGS = 'meanings'
    RELATIONS = 'relations'
    DEFINITION = 'definition'
    DEFINITION_WORDS = 'definition_words'
    MEANING_NUMBER = 'number'
    EXAMPLES = 'examples'
    SYNONYMS = 'synonyms'
    ANTONYMS = 'antonyms'
    HYPONYMS = 'hyponyms'
    HYPERNYMS = 'hypernyms'
    HOLONYMS = 'holonyms'
    MERONYMS = 'meronyms'
    TRANSLATIONS = 'translations'

    FOR_MEANINGS = 'for_meanings'

    TEXT_FORMAT = 0
    ARRAY_FORMAT = 1
    DICT_FORMAT = 2

    # languages
    ENGLISH_LANGUAGE = 'en'
    SPANISH_LANGUAGE = 'sp'
    POLISH_LANGUAGE = 'pl'

    @abc.abstractmethod
    def parse(self, text: str):
        pass


class ParserConfigurationFile:
    SYMBOLS = 'symbols.yaml'
    SETTINGS = 'settings.yaml'
    PATTERNS = 'patterns.yaml'
