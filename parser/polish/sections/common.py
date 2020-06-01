import regex as re


class ParserHelper:

    @staticmethod
    def get_number(line, pattern):
        number_match = re.search(pattern, line)
        number = None
        if number_match:
            number = number_match.group(1)
        return number

    @staticmethod
    def get_text_part(group_text):
        if '|' in group_text:
            parts = group_text.split('|')
            text_part = parts[1]
        else:
            text_part = group_text
        return text_part
