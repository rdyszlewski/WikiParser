class Meaning:

    def __init__(self, pos=None, definition=None):
        self.definition = definition
        self.part_of_speech = pos
        self.gender = None
        self.registers = []
        self.examples = []
        self.relations = []
        self.translations = []
        self.link = None


class Relation:

    def __init__(self, type=None, words=None):
        if words is None:
            words = []
        self.type = type
        self.words = words


class Translation:

    def __init__(self, language=None, translations=None):
        if translations is None:
            translations = []
        self.language = language
        self.translations = translations
