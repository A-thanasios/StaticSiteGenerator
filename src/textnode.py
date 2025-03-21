from enum import Enum

class TextType(Enum):
    TEXT = ''
    BOLD = '**'
    ITALIC = '_'
    CODE = '`'
    LINK = 5
    IMAGE = 6

    def get_text_type(delimiter):
        return next((t for t in TextType if t.value == delimiter), None)


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'