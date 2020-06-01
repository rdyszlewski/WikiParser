import click
import logging
from parser.common.file_helper import JsonSaver
from parser.common.wiktionary_parser import WiktionaryParser
from configuration.configuration import Configuration


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.argument('configuration_path')
def main(configuration_path):
    parser = WiktionaryParser(configuration_path)
    result = parser.parse()
    configuration = Configuration(configuration_path)
    JsonSaver.save_to_json(result, configuration.get_output_path())


if __name__ == "__main__":
    main()
