from email.mime import image
from math import e
from typing import Container
import flet as ft
from flet import (
    Row,
    Column,
    FilePicker,
    FilePickerResultEvent,
    icons
)
from pathlib import Path





def main(page: ft.Page):
    page.title = "Análize de Imagens"


    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"    

        for arquivo in Path(directory_path.value).iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", 'tiff'):
                directory_path.data.append(ft.Text(value=str(arquivo)))
                page.data += 1
                

        no_click(0)            
        directory_path.update()

      
    def exibir_imagens(versoes):
        imagem_botao = []
        for i in range(1,enumerate(versoes) - 1):
            imagem_botao.append( 
                Column(
                    [
                        ft.ElevatedButton(
                            f"{20*i}%",    
                            on_click=lambda _: get_directory_dialog.get_directory_path(),
                            disabled=page.web,
                        ),
                        
                        ft.Image(
                            src=imagem,  # Caminho do arquivo,
                            width=300,  # Largura da imagem
                            height=300, # Altura da imagem
                            fit=ft.ImageFit.FILL,  # Ajuste da imagem
                            border_radius=5,
                        )
                        
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                 )
            )
        
        return imagem_botao
    


        


    def no_click(j):
        
        #directory_path.data    lista 
        #imagem_original.data   index da imagem atual

        index = imagem_original.data
        imagem = directory_path.data[index]


        if  j == 0:
            index = 0
            

        if j == -1:
            if index > 0:
                index -= 1
            else:
                index = len(directory_path.data) - 1
        
          
        
        if j == 1:
            if index < len(directory_path.data) - 1:
                index = index + 1
            else:
                index = 0

        imagem_original.data = index


        imagem_original.controls[0] = ft.Image(
                        src=str(directory_path.data[index]),  # Caminho do arquivo,
                        width=300,  # Largura da imagem
                        height=200, # Altura da imagem
                        fit=ft.ImageFit.FILL,  # Ajuste da imagem
                        border_radius=5,
                    )
            
        imagem_original.update()
        page.update()

        

    #itens 
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text(data = [])

    

    imagem_original = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY, data = 0 )
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
                icon=icons.ARROW_RIGHT_ALT_ROUNDED,
                on_click=no_click(-1),
                disabled=page.web,
            ),
            imagem_original,
            ft.ElevatedButton(
                "proxima imagem",
                icon=icons.ARROW_LEFT_ROUNDED,
                on_click=no_click(1),
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
        Column(
            [
            Seleção_pasta,
            atual,
            P_B,
            blur,
            horizontal,
            final,
            ]
        )
    )

ft.app(target=main)

