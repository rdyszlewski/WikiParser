import yaml


class Configuration:

    def __init__(self, configuration_path):
        file = open(configuration_path)
        configuration = yaml.safe_load(file)
        file.close()
        self.__wiktionary_path = configuration['wiktionary_path']
        self.__output_path = configuration['output_path']
        self.__settings_folder = configuration['settings_folder']
        self.__symbols_file = configuration['symbols_file']
        self.__patterns_file = configuration['patterns_file']
        self.__parser = configuration['parser']
        self.__language = configuration['language']

    def get_wiktionary_path(self):
        return self.__wiktionary_path

    def get_output_path(self):
        return self.__output_path

    def get_symbols_path(self):
        return '{}/{}'.format(self.__settings_folder, self.__symbols_file)

    def get_patterns_path(self):
        return '{}/{}'.format(self.__settings_folder, self.__patterns_file)

    def get_parser(self):
        return self.__parser

    def get_language(self):
        return self.__language
