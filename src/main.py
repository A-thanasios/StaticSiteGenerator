import re
import sys

from copystatic import make_public
from copystatic import generate_page
from converter import markdown_to_html_node
from copystatic import generate_pages_recursive

from_path = './content'
template_html = './template.html'
to_path = './docs'
default_basepath = '/'


def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = default_basepath

    make_public()

    generate_pages_recursive(from_path,
                             template_html,
                             to_path,
                             basepath)



main()
