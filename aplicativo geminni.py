from email.mime import image
import flet as ft
from flet import Container, Row, Column, FilePicker, FilePickerResultEvent, icons
from pathlib import Path
import cv2 
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import funcoes.converta_para_png as t_p
import funcoes.corte_da_imagem as corte

# Function to convert NumPy array to base64 PNG image
def numpy_to_base64(np_array):
    image = Image.fromarray(np_array.astype('uint8'))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def main(page: ft.Page):
    page.title = "Image Analysis"
    page.scroll = True
    is_web = False  # Variável booleana para desabilitar os botões

    # Data Storage
    directory_path = ft.Text(data=[])
    imagem_original = Container(
        image_src='C:/Users/leona/OneDrive - UFSC/Imagens/robota/Caputinho.png',
        width=150, height=150, image_fit=ft.ImageFit.FILL, data=0
    )
    imagens_pb = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
    imagens_blur = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
    imagens_vales = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])
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
                    ),
                    ft.ElevatedButton(
                        text=f"Botão {i}",
                        on_click=lambda e, data=i: processar_PB(imagens_blur.data[data]), #print(f"Botão {data} clicado"),
                        disabled=is_web,
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
            imagens_pb.data[i] = thresh
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
                        on_click=lambda e, data=i: processar_vales(imagens_pb.data[data]), #print(f"Botão {data} clicado"),
                        disabled=is_web,
                    ),
                ])
            )

        print('pb ok')
        
        imagens_pb.controls = itens
        imagens_pb.update()
        P_B.update()
        page.update()
        processar_vales(imagens_pb.data[0])
        return
   
    def processar_vales(imagem):
        imagens_vales.controls.clear()
        itens = []

        for i in range(5):
            
            # Aplicar a detecção de bordas na imagem
            bordas = cv2.Canny(imagem, i*10+30, i*10+130)

 
            imagens_vales.data[i] = bordas
            base64_image = numpy_to_base64(bordas)

            itens.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=150,
                        height=150,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        on_click=lambda e, data=i: processar_horizontal(imagens_vales.data[data]), #print(f"Botão {data} clicado"),
                        disabled=is_web,
                    ),
                ])
            )


        print('vales ok')
        
        imagens_vales.controls = itens
        imagens_vales.update()
        horizontal.update()
        page.update()
        processar_horizontal(imagens_vales.data[0])
        
        return 

    def processar_horizontal(bordas):
        if imagem_original.image_src != None:
            imagem = cv2.imread(imagem_original.image_src)
        else:
            imagem = cv2.imread("C:/Users/leona/OneDrive - UFSC/Imagens/robota/Caputinho.png")
        imagens = []
        imagens_hz.controls.clear()
        itens = []

        # Detectar as linhas na imagem
        linhas = cv2.HoughLinesP(bordas, 1, np.pi/180, threshold=80, minLineLength=500, maxLineGap=1000)

        # Ordenar as linhas pela sua comprimento
        linhas_ordenadas = sorted(linhas, key=lambda linha: linha[0][2] - linha[0][0], reverse=True)

        # Retornar as 'num_linhas' maiores linhas
        L_O = linhas_ordenadas[:5]
        print(len(linhas))
        print(len(L_O))
        
        for i in range(len(L_O)):
            
            

           
            imagens.append(imagem.copy())

            x1, y1, x2, y2 = L_O[i][0]
            cv2.line(imagens[i], (x1, y1), (x2, y2), (255, 0, 0), 25)

            imagens_hz.data[i] = imagens[i]
            base64_image = numpy_to_base64(imagens[i])

            itens.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=150,
                        height=150,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        on_click=lambda e, data=i: processar_imagem_final(imagens_hz.data[data]), #print(f"Botão {data} clicado"),
                        disabled=is_web,
                    ),
                ])
            )

        print('hz ok')

        imagens_hz.controls = itens
        imagens_hz.update()
        horizontal.update()
        final.update()
        page.update()
        processar_imagem_final(imagens_hz.data[0])
        return #lines
    
    def processar_imagem_final(ima):
        imagem_final.controls.clear()
        itens = []

        
        base64_image = numpy_to_base64(ima)

        itens.append(
            ft.Column([
                ft.Image(
                    src_base64=base64_image,
                    width=150,
                    height=150,
                ),
            ])
        )

        print('final ok')
        
        imagem_final.controls = itens
        imagem_final.update()
        final.update()
        page.update()
        return


    # ... (UI elements and page setup, similar to the previous response)
    # UI Elements
    get_directory_dialog = FilePicker(on_result=get_directory_result)

    Seleção_pasta = Row([
        ft.Text(value="Escolha a pasta que deseja fazer a análize:"),
        ft.ElevatedButton(
            "Selecionar Pasta",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=is_web,
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
                disabled=is_web,
            ),
            imagem_original,
            ft.ElevatedButton(
                "proxima imagem",
                icon=icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
                on_click=proxima,
                disabled=is_web,
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
        ft.Text(value="Escolha a imagem com a melhor linha borda:"),
        imagens_vales,
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
