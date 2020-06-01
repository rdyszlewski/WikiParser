import yaml


class PolishSymbols:

    def __init__(self, configuration_path: str):
        with open(configuration_path) as file:
            configuration = yaml.safe_load(file)
        self.meanings = configuration['meanings']
        self.inflections = configuration['inflection']
        self.synonyms = configuration['synonyms']
        self.antonyms = configuration['antonyms']
        self.hypernyms = configuration['hypernyms']
        self.hyponyms = configuration['hyponyms']
        self.holonyms = configuration['holonyms']
        self.meronyms = configuration['meronyms']
        self.examples = configuration['examples']
        self.translations = configuration['translations']

        self.musculine = configuration['musculine']
        self.feminine = configuration['feminine']
        self.neutral = configuration['neutral']

        self.noun = configuration['noun']
        self.verb = configuration['verb']
        self.adjective = configuration['adjective']
        self.adverb = configuration['adverb']

        self.english = configuration['english']
        self.spanish = configuration['spanish']
        self.polish_section = configuration['polish_section']
        self.english_section = configuration['english_section']

        self.start_section = configuration['start_section']
        self.start_language_section = configuration['start_language_section']
