import pickle

from interwiktionary_mapper.dictionary import Dictionary
from interwiktionary_mapper.mapper import InterWiktionaryMapper
from parser.common.file_helper import JsonSaver
from parser.common.wiktionary_parser import WiktionaryParser
from configuration.configuration import Configuration


POLISH_PARSER_PATH = '/media/roman/SeagateExpansion/Pobrane/Wiktionary/pl_10/plwiktionary-20191001-pages-articles-multistream.xml'
ENGLISH_PARSER_PATH = '/media/roman/SeagateExpansion/Pobrane/Wiktionary/Angielska/Rozpakowane/enwiktionary-20190701-pages-articles-multistream.xml'

# POLISH_PARSER_RESULT_PATH = 'output/polish_wiki.pck'
POLISH_PARSER_RESULT_PATH = 'output/polish_wiki.pck'
ENGLISH_PARSER_RESULT_PATH = 'output/english_wiki3.pck'
POLISH_ENGLISH_PARSER_RESULT_PATH = 'output/polish_english_wiki.pck'
POLISH_REGISTER_PATH = 'output/polish_registers.txt'
ENGLISH_REGISTER_PATH = 'output/english_registers.txt'

WIKI_MAP_PATH = 'output/mapping_result.pck'


def main():
    __start_parser()
    # file = open('{}/{}'.format('configuration2/english/', ParserConfigurationFile.PATTERNS))
    # patterns = yaml.safe_load(file)
    # file.close()

def __start_parser():
    configuration_path = 'configuration/configuration.yaml'
    parser = WiktionaryParser(configuration_path)
    result = parser.parse()
    configuration = Configuration(configuration_path)
    JsonSaver.save_to_json(result, configuration.get_output_path())

def _map_inter_wiktionary():
    first_wiki_path = POLISH_ENGLISH_PARSER_RESULT_PATH
    second_wiki_path = ENGLISH_PARSER_RESULT_PATH
    mapper = InterWiktionaryMapper()
    dictionary = Dictionary()
    dictionaries = ['Fugl', 'Saloni', 'teradict', 'wiktionary', 'ISEL', 'wikipedia', 'wkuwacz-fiszka']
    dictionary.load('/media/roman/SeagateExpansion/Projects/LUMapper/resources/dictionaries/extracted', 'dict.txt',
                    dictionaries)
    result = mapper.start(first_wiki_path, second_wiki_path, dictionary)
    pickle.dump(result, open(WIKI_MAP_PATH, 'wb'))

main()