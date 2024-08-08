from email.mime import image
import flet as ft
from flet import Container, Row, Column, FilePicker, FilePickerResultEvent, icons
from pathlib import Path
import cv2 
import numpy as np
from PIL import Image
from io import BytesIO
import base64

# Function to convert NumPy array to base64 PNG image
def numpy_to_base64(np_array):
    image = Image.fromarray(np_array.astype('uint8'))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def main(page: ft.Page):
    page.title = "Image Analysis"

    # Data Storage
    directory_path = ft.Text(data=[])
    imagem_original = Container(
        image_src='C:/Users/leona/OneDrive - UFSC/Imagens/robota/Caputinho.png',
        width=150, height=150, image_fit=ft.ImageFit.FILL, data=0
    )
    imagens_pb = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
    imagens_blur = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
    imagens_hz = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
    imagem_final = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])

    # Event Handlers
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.data.clear()
        for arquivo in Path(directory_path.value).iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", '.tif'):
                new_path = str(arquivo).replace("\\", "/")
                directory_path.data.append(new_path)

        proxima(e)
        anterior(e)
        directory_path.update()
        processar_blur()
        processar_horizontal()


    def proxima(e):
        if imagem_original.data == len(directory_path.data) - 1:
            imagem_original.data = 0
        else:
            imagem_original.data += 1
        #print("pro")
        #print(directory_path.data)
        print(imagem_original.data)
        #print(directory_path.data[imagem_original.data])

        imagem_original.image_src = directory_path.data[imagem_original.data]
        imagem_original.update()
        atual.update()
        processar_blur()
        processar_horizontal()
        page.update()

    def anterior(e):
        if imagem_original.data == 0:
            imagem_original.data = len(directory_path.data) - 1
        else:
            imagem_original.data -= 1
        #print("ant")
        #print(directory_path.data)
        print(imagem_original.data)
        #print(directory_path.data[imagem_original.data])
        imagem_original.image_src = directory_path.data[imagem_original.data]
        imagem_original.update()
        atual.update()
        processar_blur()
        page.update()

    def processar_blur():
        imagens_blur.controls.clear()
        image = Image.open(imagem_original.image_src).convert('RGB')
        image = np.array(image)
        pb_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        itens = []

        for i in range(5):
            BLUR = cv2.GaussianBlur(pb_image, (1 + i*20, 1 + i*20), 0)
            imagens_blur.data[i] = BLUR
            base64_image = numpy_to_base64(BLUR)

            itens.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=150,
                        height=150,
                    ),#processar_PB(imagens_blur.data[data]),
                    ft.ElevatedButton(
                        text=f"Botão {i}",
                        on_click=lambda e, data=i: print(f"Botão {data} clicado"),
                        disabled=page.web,
                    ),
                ])
            )


        print('blur ok')
        imagens_blur.controls = itens
        imagens_blur.update()
        blur.update()
        page.update()
        processar_PB(imagens_blur.data[0])
        return blur

    def processar_PB(ima):
        #print(ima)
        imagens_pb.controls.clear()
        itens = []

        for i in range(5):
            ret,thresh = cv2.threshold(ima,(1 + (15*i)),255,0)
            imagens_blur.data[i] = thresh
            base64_image = numpy_to_base64(thresh)

            itens.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=150,
                        height=150,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        disabled=page.web,
                    ),
                ])
            )

        print('pb ok')
        
        imagens_pb.controls = itens
        imagens_pb.update()
        P_B.update()
        page.update()
        return

    def processar_horizontal():

        image = Image.open(imagem_original.image_src).convert('RGB')
        image = np.array(image)
        pb_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        itens = []

        for i in range(5):
            BLUR = cv2.GaussianBlur(pb_image, (1 + i*20, 1 + i*20), 0)
            imagens_blur.data[i] = BLUR
            base64_image = numpy_to_base64(BLUR)

            itens.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=150,
                        height=150,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        #on_click=lambda e, data=i: processar_PB(imagens_blur.data[data]),
                        disabled=page.web,
                    ),
                ])
            )

        imagens_blur.controls = itens
        imagens_blur.update()
        blur.update()
        page.update()


        #edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        #lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        #horizontal.controls = lines
        horizontal.update()
        page.update()
        return #lines

    def processar_imagem(imagem_original):
        img = cv2.imread(imagem_original)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        return lines

    # ... (UI elements and page setup, similar to the previous response)
    # UI Elements
    get_directory_dialog = FilePicker(on_result=get_directory_result)

    Seleção_pasta = Row([
        ft.Text(value="Escolha a pasta que deseja fazer a análize:"),
        ft.ElevatedButton(
            "Selecionar Pasta",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=page.web,
        ),
        directory_path,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    atual = Column(
        [
        Row([
            ft.Text(value="Imagem Atual:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        Row(
        [
            ft.ElevatedButton(
                "Imagem aterior",
                icon=icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                on_click=anterior,
                disabled=page.web,
            ),
            imagem_original,
            ft.ElevatedButton(
                "proxima imagem",
                icon=icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
                on_click=proxima,
                disabled=page.web,
            ),

        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    ])

    blur = Column([
        ft.Text(value="Escolha a imagem com o melhro blur:"),
        imagens_blur,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    P_B = Column([
        ft.Text(value="Escolha a imagem com o melhor contraste:"),
        imagens_pb,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    horizontal = Column([
        ft.Text(value="Escolha a imagem com a melhor linha horizontal:"),
        imagens_hz,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    final = Row([
        ft.Text(value="Essa é a imagem processada e esses são os valores encontrados:"),
        imagem_final,

    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )


    # Page Setup
    page.overlay.extend([get_directory_dialog])
    page.add(
        Seleção_pasta,
        atual,
        blur,
        P_B,
        horizontal,
        final,
    )

ft.app(target=main)
