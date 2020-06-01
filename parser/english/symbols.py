import yaml


class EnglishSymbols:

    def __init__(self, configuration_path: str):
        with open(configuration_path) as file:
            configuration = yaml.safe_load(file)
        self.synonyms = configuration['synonyms']
        self.hypernyms = configuration['hypernyms']
        self.hyponyms = configuration['hyponyms']
        self.translations = configuration['translations']
        self.masculine = configuration['masculine']
        self.feminine = configuration['feminine']

        self.noun = configuration['noun']
        self.verb = configuration['verb']
        self.adjective = configuration['adjective']
        self.adverb = configuration['adverb']

        self.polish = configuration['polish']
        self.english = configuration['english']
        self.spanish = configuration['spanish']
