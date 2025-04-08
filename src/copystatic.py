import os
import shutil

from converter import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, to_path, basepath):
    print(f'Generating page {from_path} to {to_path} using {template_path}')

    with open(from_path, 'r') as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    htmlstring = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace('{{ Title }}', title)
    full_html = full_html.replace('{{ Content }}', htmlstring)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    if not os.path.isdir(os.path.split(to_path)[0]):
        os.makedirs(os.path.split(to_path)[0], exist_ok=True)

    with open(to_path, 'w') as path_file:
        path_file.write(full_html)

def generate_pages_recursive(from_path, template_path, to_path, basepath):
    files = find_files(from_path)
    for file in files:
        if file.endswith('.md'):
            # Get the relative path from the content directory
            relative_path = os.path.relpath(file, from_path)

            # Create the output path by joining the destination directory with the relative path
            output_path = os.path.join(to_path, relative_path)

            # Replace the .md extension with .html
            output_path = output_path.replace('.md', '.html')

            # Make sure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Generate the page
            generate_page(file, template_path, output_path, basepath)

def find_files(directory):
    files = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            files.append(path)
        else:
            files += find_files(path)

    return files

def make_public():
    # delete content of public
    shutil.rmtree('./docs/', ignore_errors=True)
    # copy whole directory static to public
    static_files = find_files('./static/')

    os.mkdir('./docs')

    for file in static_files:
        new_file = f'./docs/{file.split('./static/', 1)[1]}'
        if not os.path.isdir(os.path.split(new_file)[0]):
            os.mkdir(os.path.split(new_file)[0])
        if not os.path.exists(new_file):
            shutil.copy(file, new_file)

