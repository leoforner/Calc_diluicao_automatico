import numpy as np
from PIL import Image
from io import BytesIO
import base64
import flet as ft

# Função para converter matriz NumPy para imagem PNG em base64
def numpy_to_base64(np_array):
    image = Image.fromarray(np_array.astype('uint8'))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Criação de uma matriz NumPy como exemplo
np_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
base64_image = numpy_to_base64(np_array)

# Função Flet para exibir a imagem
def main(page: ft.Page):
    img = ft.Image(src_base64=base64_image)
    container = ft.Container(content=img)
    page.add(container)

# Executar o aplicativo Flet
ft.app(target=main)
