import re
from bs4 import BeautifulSoup

# HTML de ejemplo
html = """
<p>
    <strong>texto texto texto </strong>
</p>
<p>
    loremipsum blabla bla biwbqeocbiweubvonbhjwbdojbvk
</p>
"""

# Patrón a buscar en el HTML
patron = re.compile(r'<p>\s*<strong>(.*?)</strong>\s*</p>')

# Nueva etiqueta a reemplazar
nueva_etiqueta = '<strong class="heading5">\\1</strong>'

# Buscar el patrón en el HTML y reemplazarlo
html_modificado = re.sub(patron, nueva_etiqueta, html)

# Parsear el HTML modificado con Beautiful Soup
soup = BeautifulSoup(html_modificado, 'html.parser')

# Imprimir el HTML modificado
print(soup.prettify())
