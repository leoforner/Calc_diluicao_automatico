import flet as ft
from flet import (
    Container,
    Row,
    Column,
    FilePicker,
    FilePickerResultEvent,
    icons
)
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv




def main(page: ft.Page):
    page.title = "Análize de Imagens"


    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"    

        for arquivo in Path(directory_path.value).iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", 'tiff'):
                new_path = str(arquivo).replace("\\", "/")
                directory_path.data.append(str(new_path))
                

        proxima(e)
        anterior(e)
        directory_path.update()
      
    def exibir_imagens(versoes):
        imagem_botao = []
        for i in range(1,len(versoes) ):

            imagem_botao.append( 
                Row(
                    [
                        Container(
                            image_src=versoes[i-1],
                            width=150,
                            height=150,
                            image_fit=ft.ImageFit.FILL,
                            #onclick = ,
                        ),
                        ft.Text( f"{20*i}%"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                 )
            )
        
        return imagem_botao
    
       
        #directory_path.data    lista 
        #imagem_original.data   index da imagem atual

    def proxima(e):
        if imagem_original.data == len(directory_path.data) - 1:
            imagem_original.data = 0
        else:
            imagem_original.data += 1
        print("pro")
        print(directory_path.data)
        print(imagem_original.data)
        print(directory_path.data[imagem_original.data])

        imagem_original.image_src = directory_path.data[imagem_original.data]
            
        imagem_original.update()
        atual.update()
        page.update()       

    def anterior(e):
        if imagem_original.data == 0:
            imagem_original.data = len(directory_path.data) - 1
        else:
            imagem_original.data -= 1
        print("ant")
        print(directory_path.data)
        print(imagem_original.data)
        print(directory_path.data[imagem_original.data])
        imagem_original.image_src = directory_path.data[imagem_original.data]
            
        imagem_original.update()
        atual.update()
        page.update()


    def processar_PB(imagem_original):
        img = cv2.imread(imagem_original, cv2.IMREAD_GRAYSCALE)
        return img

    def processar_blur(imagem_original):
        img = cv2.imread(imagem_original)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        return blur

    def processar_horizontal(imagem_original):
        img = cv2.imread(imagem_original)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        return lines

    def processar_imagem(imagem_original):
        img = cv2.imread(imagem_original)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        return lines
    
    




    #itens 
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text(data = [])

    

    imagem_original = Container( image_src='C:/Users/leona/OneDrive - UFSC/Imagens/robota/Caputinho.png', width=150, height=150, image_fit=ft.ImageFit.FILL, data = 0 )
    
    
    imagens_pb = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
    
    
    imagens_blur = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
    
    
    imagens_hz = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )


    #linhas 
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
    
    P_B = Column([ 
        ft.Text(value="Escolha a imagem com o melhor contraste:"),
        imagens_pb,
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

    blur = Column([ 
        ft.Text(value="Escolha a imagem com o melhro blur:"),
        imagens_blur,
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
        
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
  
    
    

    
    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])



    page.add(

            Seleção_pasta,
            atual,
            P_B,
            blur,
            horizontal,
            final,

    )

ft.app(target=main)

