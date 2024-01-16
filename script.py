from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

documents_path = os.path.expanduser("~/Documents")

# Configuración del navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado y su ruta en el PATH
driver.get("https://ahrefs.com/writing-tools/img-alt-text-generator")  # Reemplaza 'URL_DE_TU_PAGINA' con la URL real

# Carpeta con las imágenes
carpeta_imagenes = documents_path + "/html/"  # Reemplaza 'RUTA_DE_TU_CARPETA' con la ruta real

# Archivo de salida para los resultados
archivo_resultados = "resultados.txt"

# Itera sobre las imágenes en la carpeta
for imagen_nombre in os.listdir(carpeta_imagenes):
    # Ignorar archivos HTML
    if not imagen_nombre.lower().endswith(('.html', '.htm')):
        # Encuentra el campo de tipo archivo y el botón
        div_contenedor = driver.find_element("div[data-hidden-mobile='true'][data-hidden-tablet='true'][data-hidden-desktop='true']")
        campo_imagen = div_contenedor.find_element("input[type='file']")
        boton_enviar = driver.find_element_by_css_selector('.css-ljl0n3-button.css-rxvlhs-buttonAlignContent.css-ohx8vg-buttonColor.css-1r4vxsw.css-emomfn')  # Reemplaza con tu clase CSS real

        # Ruta completa de la imagen
        ruta_imagen = os.path.join(carpeta_imagenes, imagen_nombre)

        # Cargar la imagen en el campo de tipo archivo
        campo_imagen.send_keys(ruta_imagen)

        # Enviar el formulario
        boton_enviar.send_keys(Keys.RETURN)

        # Esperar a que se cargue la página (puedes ajustar el tiempo según sea necesario)
        time.sleep(5)

        # Obtener el resultado y escribir en el archivo
        resultado = driver.find_element_by_css_selector('TU_SELECTOR_DEL_RESULTADO').text  # Reemplaza 'TU_SELECTOR_DEL_RESULTADO' con el selector real
        with open(archivo_resultados, "a") as f:
            f.write(f"Imagen: {imagen_nombre}\nResultado: {resultado}\n\n")

# Cerrar el navegador al final
driver.quit()