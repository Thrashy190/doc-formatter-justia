import os
import re
import datetime
import mammoth
import shutil
import time
from bs4 import BeautifulSoup
from docx import Document
from PIL import Image
from urllib.parse import urlparse, urlunparse
from progress.bar import Bar
from alive_progress import alive_bar

style_map = """
    p[style-name='Heading 1'] => strong.heading1:fresh
    p[style-name='Title'] => strong.heading1:fresh
    p[style-name='Heading 2'] => strong.heading4:fresh
    p[style-name='Heading 3'] => strong.heading5:fresh
"""

def remove_special_chars(string):
    # Utilizamos una expresión regular para encontrar y eliminar caracteres especiales
    cadena_sin_especiales = re.sub(r'[^a-zA-Z0-9 ]', '', string)
    return cadena_sin_especiales

def process_links(html_content, site):
    # Lógica para procesar las URLs en el contenido HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')

        # Verifica si la URL contiene la cadena específica
        if site in href:
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

def extract_images(docx_file_path, output_folder,target_size=(300, 200)):
    document = Document(docx_file_path)
    image_count = 1
    #with alive_bar(len([rel for rel in document.part.rels.values()  if "image" in rel.reltype and "media" in rel.target_ref])) as bar: 
    for rel in document.part.rels.values():
        if "image" in rel.reltype and "media" in rel.target_ref:
            image_data = rel.target_part.blob
            image_name = f"image_{image_count}.jpg"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, "wb") as image_file:
                image_file.write(image_data)

            # Redimensionar la imagen
            resize_image(image_path, target_size)
            ##print(f"Extracted image {image_count}: {image_name}")
            image_count += 1
                #bar() 

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


def search_titles(html):
    soup = BeautifulSoup(html,"html.parser")
    heading4_tags = soup.find_all("strong", {"class": "heading4"})
    heading5_tags = soup.find_all("strong", {"class": "heading5"})

    for heading in heading4_tags:
        heading.string.replace_with(capitalize_title(heading.get_text()))
    
    for heading in heading5_tags:
        heading.string.replace_with(capitalize_title(heading.get_text()))
       
    return soup


def capitalize_title(title):
    """This is a function that capitalizes automatically H1 titles for pages and blog posts.

    We have two arrays :

        1. Exclusions: Words that, unless they're the first letter of the title, must not be capitalized.
        2. Acronyms: Acronyms must always be capitalized so on this array we save acronyms I got from this site: https://www.justice.gov/nsd-ovt/us-government-acronym-list

    Args:
        title (string): The only argument it takes is the title of the post or page as string.

    Returns:
        capitalized_heading (string): It returns as string the title correctly capitalized.
    """
    exclusions = [
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "en",
        "for",
        "if",
        "in",
        "nor",
        "of",
        "on",
        "or",
        "per",
        "the",
        "to",
        "v.",
        "vs.",
        "via",
    ]
    acronyms = [
        "AAG",
        "ACS",
        "ADIC",
        "AG",
        "AG Guidelines",
        "ALAT",
        "ASAC",
        "ASG",
        "ATAC",
        "ATF",
        "AUSA",
        "BOP",
        "CCIPS",
        "CEOS",
        "CES",
        "CFR",
        "CIA",
        "CIPA",
        "CJPAF",
        "CTS",
        "CVRA",
        "DAG",
        "DEA",
        "DOD",
        "DOJ",
        "DOS",
        "DSS",
        "DUI"
        "DWI"
        "EOUSA",
        "EWAP",
        "FAA",
        "FARA",
        "FAUSA",
        "FBI",
        "FIRS",
        "FISA",
        "FOIA",
        "FY",
        "GAO",
        "GSA",
        "HRSP",
        "IC",
        "ICITAP",
        "INTERPOL",
        "IRS",
        "ITVERP",
        "JFK",
        "JM",
        "JMD",
        "JTTF",
        "LEGAT",
        "MLARS",
        "MLAT",
        "MOU",
        "NCIS",
        "NCTC",
        "NSD",
        "OARM",
        "ODNI",
        "OI",
        "OIA",
        "OIG",
        "OIP",
        "OJP",
        "OLA",
        "OLC",
        "OLE",
        "OMC",
        "OMB",
        "OPA",
        "OPDAT",
        "OPM",
        "OPR",
        "OSHA"
        "OVC",
        "OVT",
        "SAC",
        "SAUSA",
        "SB",
        "SG",
        "STEP",
        "UCMJ",
        "USA",
        "USAOs",
        "USC",
        "USDC",
        "USMS",
        "USSG",
        "USVSST",
        "VA",
        "VOCA",
        "VRRA",
        "VSD",
        "VTC",
        "VWA",
        "VWC",
    ]
    # We turn all words of the title lowercased and convert it into an array of words.
    words = title.lower().split(" ")

    # Empty array on which we'll store our modified words.
    capitalized_heading = []

    # If the title has a '.' at the end of the last word, it gets removed since headings should not have '.'
    if words[-1].endswith("."):
        words[-1] = words[-1][:-1]

    # We iterate over every word of the title.
    for i in range(len(words)):
        # We capitalize the first letter of each title and append it into our capitalized_heading array.
        if i == 0:
            capitalized_heading.append(words[i].capitalize())

        # We check if any word has a hyphen as in a-b and capitalize both 'parts' of the hyphenated words append it into our capitalized_heading array.
        elif "-" in words[i]:
            parts = words[i].split("-")
            capitalized_parts = [part.capitalize() for part in parts]
            words[i] = "-".join(capitalized_parts)
            capitalized_heading.append(words[i])

        # Check if the word is not on the exclusions array and if true, then it capitalize the word and append it into our capitalized_heading array.
        elif words[i] not in exclusions:
            capitalized_heading.append(words[i].capitalize())

        # If the word did not meet the conditions above it's appended into our capitalized_heading array.
        else:
            capitalized_heading.append(words[i])

    # Here we iterate over our capitalize heading to check for acronyms on each word and colons on the title.
    for i in range(len(capitalized_heading)):
        # Here we check if indeed an acronym is found uppercasing the word of the array and looking for it on the acronyms array and only then we capitalize it.
        if capitalized_heading[i].upper() in acronyms:
            capitalized_heading[i] = capitalized_heading[i].upper()

        # Checks if a colon is at the end of any word and if the very next word is on the exclusions it's capitalized
        if (
            capitalized_heading[i].endswith(":")
            and capitalized_heading[i - 1] in exclusions
        ):
            capitalized_heading[i + 1] = capitalized_heading[i + 1].capitalize()

    # Join the array into a string separated by spaces.
    return " ".join(capitalized_heading)


def get_h1_heading(html):
    soup = BeautifulSoup(html,"html.parser")
    heading1 = soup.find("strong",{"class": "heading1"})
    text = heading1.get_text(strip=True)

    soup.find("strong",{"class": "heading1"}).decompose()

    return text


def fix_strong_heading(file_name, html):
    # Patrón a buscar en el HTML
    patron = re.compile(r'<p>\s*<strong>(.*?)</strong>\s*</p>')

    # Nueva etiqueta a reemplazar
    nueva_etiqueta = '<strong class="heading5">\\1</strong>'

    # Función para registrar el hallazgo del patrón
    def log_hallazgo():
        now = datetime.datetime.now()
        with open("logfile.log", "a") as log_file:
            log_file.write(f"[{now}] - {file_name} - Bad format for subheading strong title\n")

    # Buscar el patrón en el HTML y reemplazarlo
    html_modificado, num_reemplazos = re.subn(patron, nueva_etiqueta, html)
    if num_reemplazos > 0:
        log_hallazgo()

    return html


def start():
    directory = "ATU-31648-574"
    site = 'https://www.moseleycollins.com/'
    #site = "https://www.reynoldsdefensefirm.com/"
    documents_path = os.path.expanduser("~/Documents") + '/justia/'
    output_folder_path = documents_path + directory +"/html"
    output_folder_img_path = documents_path + directory +"/img"
    not_formatted=[]
    formatted=[]
    data = []
    error = []
    count = 0

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

        shutil.rmtree(documents_path + directory + "/img/", ignore_errors=True)
        os.mkdir(documents_path + directory + "/img/")
        #with Bar('Processing...',max=len([entry for entry in os.listdir(documents_path + directory + '/files') if os.path.isfile(os.path.join(documents_path + directory + '/files', entry))])) as bar: 
        for entry in entries:

            if entry.name == "html" or entry.name == ".DS_Store" or entry.name == "img":
                continue

            print(f"{entry.name}")
            with open(documents_path  + directory + '/files/'+entry.name, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file.name, style_map=style_map)

            name = entry.name.replace(".docx",".html") 
            name = name.replace(" ","_")
            

            

            video = """
                    <div class="responsive-video">
                        <div class="video-wrapper">
                            <iframe allow="autoplay; fullscreen; picture-in-picture" allowfullscreen="" data-ready="true" frameborder="0" src="https://player.vimeo.com/video/718373605?h=544f9ab318&amp;title=0&amp;byline=0&amp;portrait=0" width="100%" height="315"></iframe> 
                        </div>
                    </div>
                    """
            # add video on the top of the file
            result.value = get_h1_heading(result.value) + video + result.value

            #result.value = search_titles(result.value)

            result.value = fix_strong_heading(name,str(result.value))

            result.value = add_class_to_ul(str(result.value))
            result.value = remove_a_id(result.value)
            result.value = process_links(result.value,site)
            

            # Extract images and update img tags in HTML
            image_count = extract_images(docx_file.name, output_folder_img_path)
            soup = BeautifulSoup(result.value, "html.parser")

            for index,img_tag in enumerate(soup.find_all("img")):
                # Buscar el elemento strong más cercano
                try:
                    alt_text = img_tag.find_next("strong").get_text(strip=True)
                except:
                    alt_text = str(int(time.time()))

                next_text = remove_special_chars(alt_text)
                next_text = "-".join(e for e in list(map(str.lower,next_text.split(" "))))
                time.sleep(1)
                img_name = f"{next_text}-{str(int(time.time()))}.jpg"
                # Usar el texto como nombre de la imagen
                img_path = os.path.join(output_folder_img_path, img_name)

                # width="300px" height="200px" amp-position="right" class="right amp-include"
                # Agregar el atributo alt a la imagen con el texto del strong
                img_tag["alt"] = alt_text
                img_tag["width"] = "300"
                img_tag["height"] = "200"
                img_tag["amp-position"] = "right"
                img_tag["class"] = "right amp-include"

                # Renombrar la imagen
                try:
                    os.rename(os.path.join(output_folder_img_path, f"image_{index+1}.jpg"), img_path)
                except FileNotFoundError:
                    error.append({"name":name,"image":index+1})
                img_tag["src"] = f"photos/{img_name}"

            # Save the modified HTML
            html_output_path = os.path.join(output_folder_path, name)
            with open(html_output_path, "w", encoding="utf-8") as html_file:
                html_file.write(str(soup))

            #bar.next() 
            count = 1 + count

        print("Paginas totales:" + str(count))  
        if len(error) > 0:
            print("Error List")

        for data in error:
            print(f"File:{data['name']}, Image {data['image']} not found")
            


start()