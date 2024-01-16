import os
import mammoth
import shutil
import typer
from PyInquirer import prompt
from bs4 import BeautifulSoup
from docx import Document
from PIL import Image


class Converter:
    def __init__(output_folder_path, input_folder_path, self) -> None:
        self.output_folder_path = output_folder_path
        self.input_folder_path = input_folder_path