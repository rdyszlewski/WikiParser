import abc


class Analyzer():
    WORD = 0
    POS = 1

    @abc.abstractmethod
    def analyse(self, sentence):
        pass

    @abc.abstractmethod
    def get_base_words(self, sentence):
        pass
