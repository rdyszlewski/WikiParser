import time
import xml.etree.ElementTree as ET

from parser.common.values import Languages
from configuration.configuration import Configuration
from parser.english.parser import EnglishWiktionaryParser
from parser.polish.parser import PolishWiktionaryParser
import logging

_TITLE = 'title'
_START = 'start'
_TEXT = 'text'
_END = 'end'


class WiktionaryParser:

    def __init__(self, configuration_path):
        self._configuration = Configuration(configuration_path)
        self._parser = self.__create_parser(self._configuration)

    @staticmethod
    def __create_parser(configuration: Configuration):
        parser = None
        language = configuration.get_parser()
        if language == Languages.ENGLISH:
            parser = EnglishWiktionaryParser(configuration)
        elif language == Languages.POLISH:
            parser = PolishWiktionaryParser(configuration)
        return parser

    def parse(self):
        logging.info('Start parser')
        start_time = time.time()
        events = {'start', 'end'}
        parser_result = {}
        last_page_title = None
        wiktionary_path = self._configuration.get_wiktionary_path()
        for event, elem in ET.iterparse(wiktionary_path, events=events):
            tag = self.__get_tag(elem)
            if self.__is_start_title(tag, event):
                last_page_title = elem.text
            elif tag == _TEXT and elem.text:
                text = elem.text
                if text:
                    result = self._parser.parse_text(text, last_page_title, parser_result)
                    if result:
                        parser_result[last_page_title] = result
            elem.clear()
        end_time = time.time()
        logging.info('Parsing time: {} s'.format(end_time - start_time))
        return parser_result

    @staticmethod
    def __get_tag(elem):
        return elem.tag.split('}')[1]

    @staticmethod
    def __is_start_title(tag, event):
        return tag == _TITLE and event == _START

    @staticmethod
    def __is_end_text(tag, event):
        return tag == _TEXT and event == _END
