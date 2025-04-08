import re

from copystatic import make_public
from copystatic import generate_page
from converter import markdown_to_html_node
from copystatic import generate_pages_recursive


def main():
    make_public()
    generate_pages_recursive('./content',
                  './template.html',
                  './public')



main()
