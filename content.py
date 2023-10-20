from bs4 import BeautifulSoup

content_start = '''
<div class="box">
	<strong class="heading4 tcenter">Contents</strong>
'''
content_end='</div>'


file = open("index.html","r")

soup = BeautifulSoup(file.read(), 'html.parser')
headings4 = soup.find_all('strong',{"class":"heading4"})
headings6 = soup.find_all('strong',{"class":"-darker heading6"})

def listifier(arr):
    list_start='<ul class="no-spacing-list" id="top">'
    list_end='</ul>'
    lista=""
    for tag in arr:
        lista = lista + '<li><a href="#">' + tag.getText() + '</a></li>'

    list_start = list_start +lista+list_end

    return list_start

formatedFile = open("formated.html","w")
formatedFile.write(content_start + listifier(headings4) +content_end)


print(content_start + listifier(headings4) +content_end)
#=print(listifier(headings6))