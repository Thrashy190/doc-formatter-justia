import os
import mammoth
import shutil
import time
# import typer
# from PyInquirer import prompt
from bs4 import BeautifulSoup
from docx import Document
from PIL import Image

style_map = """
    p[style-name='Heading 2'] => strong.heading4:fresh
    p[style-name='Heading 3'] => strong.heading5:fresh
"""

def extract_images(docx_file_path, output_folder,target_size=(300, 200)):
    document = Document(docx_file_path)
    image_count = 1
    for rel in document.part.rels.values():
        if "image" in rel.reltype and "media" in rel.target_ref:
            image_data = rel.target_part.blob
            image_name = f"image_{image_count}.jpg"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, "wb") as image_file:
                image_file.write(image_data)

            # Redimensionar la imagen
            resize_image(image_path, target_size)
            print(f"Extracted image {image_count}: {image_name}")
            image_count += 1

    return image_count   # Return the total number of images

def resize_image(image_path, target_size):
    image = Image.open(image_path)
    resized_image = image.resize(target_size)
    resized_image.save(image_path)

def find_closest_strong(tag):
    # Buscar hacia arriba en el árbol DOM para encontrar el elemento más cercano con la etiqueta strong
    while tag and tag.name != 'strong':
        tag = tag.parent
    return tag.text if tag else ''  # Devolver una cadena vacía si no se encuentra el elemento strong

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
        a_tag["target"] = "_blank"
        a_tag.extract()
    
    return str(soup)

# app = typer.Typer()

# @app.command()s
def start():
    directory = "abi"
    documents_path = os.path.expanduser("~/Documents") + '/Personal/proyectos/justia/'
    output_folder_path = documents_path + directory +"/html"
    not_formatted=[]
    formatted=[]
    data =[]
    error = []

    with os.scandir(documents_path) as entries:
        for entry in entries:
            if entry.name == ".DS_Store" or entry.name=="code":
                continue
            with os.scandir(documents_path + entry.name + "/") as files:
                data=[]
                for file in files:
                    data.append(file.name)  
                if "html" in data:
                    formatted.append({"name":entry.name})
                else:
                    not_formatted.append({"name":entry.name})


    with os.scandir(documents_path + directory + '/files') as entries:
        shutil.rmtree(documents_path + directory + "/html/", ignore_errors=True)
        os.mkdir(documents_path + directory + "/html/")
        for entry in entries:

            if entry.name=="html" or entry.name==".DS_Store":
                continue

            print(entry.name)
            with open(documents_path  + directory + '/files/'+entry.name, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file.name, style_map=style_map)

            name = entry.name.replace(".docx",".html") 
            name = name.replace(" ","_")
            
            video ='<div class="video-wrapper"><iframe src="https://player.vimeo.com/video/718373605?h=544f9ab318&amp;title=0&amp;byline=0&amp;portrait=0" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen="" data-ready="true" width="100%"></iframe></div>'
            # add video on the top of the file
            result.value = video + result.value

            process = add_class_to_ul(result.value)
            process = remove_a_id(process)

            # Extract images and update img tags in HTML
            image_count = extract_images(docx_file.name, output_folder_path)
            soup = BeautifulSoup(process, "html.parser")

            for index,img_tag in enumerate(soup.find_all("img")):
                # Buscar el elemento strong más cercano
                alt_text = img_tag.find_next("strong").get_text(strip=True)

                next_text = "-".join(e for e in list(map(str.lower,img_tag.find_next("strong").get_text(strip=True).split(" "))) if e.isalpha)

                if next_text == "frequently-asked-questions-(faqs)":
                    img_name = f"{next_text}-{str(int(time.time()))}.jpg"
                 # Usar el texto como nombre de la imagen
                else:
                    img_name = f"{next_text}.jpg"
                img_path = os.path.join(output_folder_path, img_name)

# width="300px" height="200px" amp-position="right" class="right amp-include"
                # Agregar el atributo alt a la imagen con el texto del strong
                img_tag["alt"] = alt_text
                img_tag["width"] = "300"
                img_tag["height"] = "200"
                img_tag["amp-position"] = "right"
                img_tag["class"] = "right amp-include"

                # Renombrar la imagen
                try:
                    os.rename(os.path.join(output_folder_path, f"image_{index+1}.jpg"), img_path)
                except FileNotFoundError:
                    error.append({"name":name,"image":index+1})
                img_tag["src"] = f"photos/{img_name}"

            # Save the modified HTML
            html_output_path = os.path.join(output_folder_path, name)
            with open(html_output_path, "w", encoding="utf-8") as html_file:
                html_file.write(str(soup))
            
        if len(error) > 0:
            print("Error List")

        for data in error:
            print(f"File:{data['name']}, Image {data['image']} not found")
            

if __name__ == "__main__":
    start()



