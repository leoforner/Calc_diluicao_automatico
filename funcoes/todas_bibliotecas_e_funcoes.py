# Função: Importar todas as bibliotecas e funções necessárias para o projeto
# bibliotecas padrão
import flet as ft
from flet import Container, Row, Column, FilePicker, FilePickerResultEvent, icons
from pathlib import Path
import cv2 
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from sympy import im
import matplotlib.pyplot as plt
import os
from rembg import remove

# bibliotecas personalizadas
from corte_da_imagem import crop
from converta_para_png import convert_tiff_to_png
from calculo_pixels_por_mm import calculate_pixels_per_mm
from calculo_da_area import calculate_area