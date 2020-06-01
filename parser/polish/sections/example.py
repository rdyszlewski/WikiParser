from parser.polish.sections.section import SectionParser


class ExampleParser(SectionParser):

    def __init__(self, patterns, symbols):
        super().__init__(patterns, symbols)

    def parse(self, section_text):
        return self._parse_section(section_text)
