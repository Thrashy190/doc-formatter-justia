import mammoth


with open("test.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
with open("sample.html", "w") as html_file:
    html_file.write(result.value)