class ParserHelper:

    @staticmethod
    def is_end_of_section(current_line, index, text_lines_length):
        return not current_line.startswith('=') and index < text_lines_length - 1

    @staticmethod
    def is_special_title(title):
        return title and '/' in title and 'translations' in title
