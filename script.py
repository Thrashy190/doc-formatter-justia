import mammoth
import os
import shutil
import sys
from bs4 import BeautifulSoup

style_map = """
    p[style-name='Heading 2'] => strong.heading4:fresh
    p[style-name='Heading 3'] => strong.heading5:fresh
"""
def add_class_to_ul(html):
    soup = BeautifulSoup(html, 'html.parser')
    for ul in soup.find_all('ul'):
        ul['class'] = ['no-spacing-list']  # Agrega la clase a todas las listas no ordenadas
    return str(soup)

def remove_a_id(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags_with_id = soup.find_all('a', id=True)
    
    for a_tag in a_tags_with_id:
        a_tag.extract()
    
    return str(soup)

def start(directory):

    with os.scandir(os.path.join(directory)) as entries:
        shutil.rmtree(os.path.join(directory, 'html'), ignore_errors=True)
        os.makedirs(os.path.join( directory, 'html'))
        for entry in entries:
            if entry.name == "html":
                continue

            print(entry.name)
            with open(os.path.join(directory, entry.name), "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file.name, style_map=style_map)

            name = entry.name.replace(".docx", ".html")
            name = name.replace(" ", "_")

            process = add_class_to_ul(result.value)
            process = remove_a_id(process)

            with open(os.path.join(directory, 'html', name), "w") as html_file:
                html_file.write(process)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py NOMBRE_DE_LA_CARPETA")
        sys.exit(1)
    directory = sys.argv[1]
    print(directory)

    components = directory.split("/")
    print(components)
    #start(directory)
