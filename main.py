from PyInquirer import prompt, Separator
import mammoth
import os
import shutil
import typer
import subprocess
from bs4 import BeautifulSoup


style_map = """
    p[style-name='Heading 2'] => strong.heading4:fresh
    p[style-name='Heading 3'] => strong.heading5:fresh
"""
def add_class_to_ul(html):
    soup = BeautifulSoup(html, 'html.parser')

    for ul_tag in soup.find_all('ul'):
            should_exclude_class = False

            # Verifica cada elemento <li> dentro del <ul>
            for li_tag in ul_tag.find_all('li'):
                # Verifica si la longitud del texto es mayor a 80 caracteres
                if len(li_tag.get_text(strip=True)) > 80:
                    should_exclude_class = True
                    break  # No es necesario verificar los demás elementos si uno ya supera los 80 caracteres

            # Agrega la clase solo si ningún <li> supera los 80 caracteres
            if not should_exclude_class:
                ul_tag['class'] = ul_tag.get('class', []) + ['no-spacing-list']

    return str(soup)

def remove_a_id(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags_with_id = soup.find_all('a', id=True)
    
    for a_tag in a_tags_with_id:
        a_tag.extract()
    
    return str(soup)

#app = typer.Typer()

# @app.command()
def start():

    documents_path = os.path.expanduser("~/Documents")
    not_formatted=[]
    formatted=[]
    data =[]

    with os.scandir(documents_path + '/justia/') as entries:
        for entry in entries:
            if entry.name == ".DS_Store" or entry.name=="code":
                continue
            with os.scandir(documents_path + '/justia/'+ entry.name + "/") as files:
                data=[]
                for file in files:
                    data.append(file.name)  
                if "html" in data:
                    formatted.append({"name":entry.name})
                else:
                    not_formatted.append({"name":entry.name})

    status = [
        {
            'type': 'list',
            'name': 'status',
            'message': 'Select the status of the directory',
            'choices': [{"name":"New"},{"name":"Formatted"}],
        }
    ]

    formatted_options = [
        {
            'type': 'list',
            'name': 'dir',
            'message': 'Select the new directory',
            'choices': formatted,
        }
    ]

    not_formatted_options = [
        {
            'type': 'list',
            'name': 'dir',
            'message': 'Format again directory',
            'choices': not_formatted,
        }
    ]

    status = prompt(status)["status"]

    if status == "New":
        directory = prompt(not_formatted_options)["dir"]
    else:
        directory = prompt(formatted_options)["dir"]


    with os.scandir(documents_path + '/justia/' + directory + '/files') as entries:
        shutil.rmtree(documents_path + "/justia/" + directory + "/html/", ignore_errors=True)
        os.mkdir(documents_path + "/justia/" + directory + "/html/")
        for entry in entries:


            if entry.name=="html":
                continue

            print(entry.name)
            with open(documents_path + '/justia/' + directory + '/files/'+entry.name, "rb") as docx_file:
                print(docx_file)
                result = mammoth.convert_to_html(docx_file.name,style_map=style_map)

            name = entry.name.replace(".docx",".html") 
            name = name.replace(" ","_")

            process = add_class_to_ul(result.value)
            process = remove_a_id(process)

            with open(documents_path + "/justia/" + directory + "/html/"+name, "w") as html_file:
                html_file.write(process)

# @app.command()
# def hola():
#     print("hola")

if __name__ == "__main__":
    # app()
    start()
