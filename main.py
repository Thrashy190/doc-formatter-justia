from PyInquirer import prompt, Separator
import mammoth
import os
import shutil
import typer
import subprocess
from bs4 import BeautifulSoup

style_map = """
    p[style-name='Heading 2'] => strong.heading4:fresh
    p[style-name='Heading 3'] => strong:fresh
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

app = typer.Typer()

@app.command()
def start():

    documents_path = os.path.expanduser("~/Documents")
    dirs=[]

    with os.scandir(documents_path + '/justia/') as entries:
        for entry in entries:
            dirs.append({"name":entry.name})

    options = [
        {
            'type': 'list',
            'name': 'dir',
            'message': 'Select the directory',
            'choices': dirs,
        }
    ]

    directory = prompt(options)["dir"]

    print(directory)

    with os.scandir(documents_path + '/justia/' + directory + '/files') as entries:
        shutil.rmtree(documents_path + "/justia/" + directory + "/html/", ignore_errors=True)
        os.mkdir(documents_path + "/justia/" + directory + "/html/")
        for entry in entries:

            if entry.name=="html":
                continue

            print(entry.name)
            with open(documents_path + '/justia/' + directory + '/files/'+entry.name, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file.name,style_map=style_map)

            name = entry.name.replace(".docx",".html") 
            name = name.replace(" ","_")

            process = add_class_to_ul(result.value)
            process = remove_a_id(process)

            with open(documents_path + "/justia/" + directory + "/html/"+name, "w") as html_file:
                html_file.write(process)

@app.command()
def hola():
    print("hola")

if __name__ == "__main__":
    app()
