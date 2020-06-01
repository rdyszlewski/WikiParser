class Dictionary:

    def __init__(self):
        self.__dictionary = {}

    def load(self, root_path, dict_name, folders):
        for folder in folders:
            path = '{}/{}/{}'.format(root_path, folder, dict_name)
            self._load_dictionary(path)

    def _load_dictionary(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                word, translation = [it.strip() for it in line.split('\t', 1)]
                if word not in self.__dictionary:
                    self.__dictionary[word] = set()
                self.__dictionary[word].add(translation)

    def get_translations(self, word):
        if word in self.__dictionary:
            return self.__dictionary[word]
        return []
