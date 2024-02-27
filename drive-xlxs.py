import os
import xlsxwriter

def main():
    workbook = xlsxwriter.Workbook('pages.xlsx')
    worksheet = workbook.add_worksheet()
    directory = "frankl_kominsky_practice_areas_1-26-24"
    full_path = os.path.expanduser("~/Documents") + '/justia/' + directory
    row = 1
    col = 0
    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Type', bold)
    worksheet.write('B1', 'City', bold)

    with os.scandir(full_path) as pages:
        for index, page in enumerate(pages):
            worksheet.write(row, col,     page.name.split(".")[0].split("Lawyers Serving")[0])
            worksheet.write(row, col + 1, page.name.split(".")[0].split("Lawyers Serving")[1])
            worksheet.checl
            row += 1 


    workbook.close()

if __name__ == "__main__":
    main()