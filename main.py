import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urlparse, urlunparse

def cambiar_encabezados(html):
    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Cambiar los elementos h2
    for h2_tag in soup.find_all('h2'):
        strong_tag = soup.new_tag('strong', **{'class': 'heading4'})
        strong_tag.string = h2_tag.string
        h2_tag.replace_with(strong_tag)

    # Cambiar los elementos h3
    for h3_tag in soup.find_all('h3'):
        strong_tag = soup.new_tag('strong', **{'class': 'heading5'})
        strong_tag.string = h3_tag.string
        h3_tag.replace_with(strong_tag)

    # Devolver el HTML modificado
    return str(soup)


def process_links(html_content):
    # Lógica para procesar las URLs en el contenido HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')

        # Verifica si la URL contiene la cadena específica
        if 'https://justia-moseleycollins-com.justia.net/' in href:
            # Elimina la parte no deseada y conserva la última parte de la ruta
            url_parts = list(urlparse(href))
            url_parts[1] = ''  # Elimina el esquema y la parte de red
            url_parts[2] = url_parts[2].split('/')[-1]  # Conserva la última parte de la ruta
            new_href = urlunparse(url_parts)

            # Actualiza el atributo href en la etiqueta <a>
            a_tag['href'] = new_href
        else:
            # Agrega el atributo target="_blank" si la URL no contiene la cadena específica
            a_tag['target'] = '_blank'

    # Devuelve el contenido HTML modificado
    return str(soup)

def download_and_save_image(img_src, output_folder,target_size=(300, 200)):
    if img_src:

        if "https://images.surferseo.art/" in img_src:

            response = requests.get(img_src)
            
            if response.status_code == 200:
                img_name_ext = os.path.basename(img_src).split(".")
                path = os.path.join(output_folder, f"{img_name_ext[0]}.jpg")
                with open(path, 'wb') as handler:
                    handler.write(response.content)

                resize_image(path, target_size)
            
def resize_image(image_path, target_size):
    try:
        image = Image.open(image_path)
        resized_image = image.resize(target_size)
        resized_image.save(image_path)
    except:
        pass

def start():
    directory = "HXL-36415-665-surfero"
    documents_path = os.path.expanduser("~/Documents") + '/justia/'
    output_folder = documents_path + directory +"/result/"
    count = 0

    with os.scandir(documents_path + directory + '/html') as entries:
        for entry in entries:
            with open(documents_path  + directory + '/html/'+entry.name, "rb") as html_file:
                soup = BeautifulSoup(html_file.read())
                for img_tag in soup.find_all('img'):
                    img_src = img_tag.get('src', '')
                    download_and_save_image(img_src, output_folder)
                    name = list(img_src.split("/"))[-1]
                    img_name_ext = f"{os.path.basename(img_src).split('.')[0]}.jpg"
                    img_tag["src"] = f"photos/{img_name_ext}"
                    print(img_name_ext)
                
                process = process_links(str(soup))
                process = cambiar_encabezados(process)



            with open(documents_path  + directory + '/html/'+entry.name, "w") as html_file:
                html_file.write(process)


            count = count + 1

    print(f"Paginas totales: {count}")


if __name__ == "__main__":
    start()


