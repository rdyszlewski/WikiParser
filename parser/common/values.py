class Gender:
    MUSCULINE = 0
    FEMININE = 1
    NEUTRAL = 2
    LACK = -1


class PartOfSpeech:
    NOUN = 0
    VERB = 1
    ADJECTIVE = 2
    ADVERB = 3
    LACK = -1


class Languages:
    POLISH = 'pl'
    ENGLISH = 'en'
    SPANISH = 'sp'


class RelationTypes:
    SYNONYMS = 'synonyms'
    ANTONYMS = 'antonyms'
    HYPONYMS = 'hyponyms'
    HYPERNYMS = 'hypernyms'
    HOLONYMS = 'holonyms'
    MERONYMS = 'meronyms'

class Sections:
    NOT_SUPPORTED = -1
    LANGUAGE = 0
    MEANINGS = 1
    RELATIONS = 2
    TRANSLATIONS = 3
