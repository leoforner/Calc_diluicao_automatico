from email.mime import image
from math import e
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
                fotos_path.controls.append(ft.Text(value=str(arquivo)))

        no_click(0)            
        directory_path.update()

    '''    
    def exibir_imagens(versoes):
        
        imagens.controls.clear()
        for imagem in versoes: 
            ft.ElevatedButton(
                icon=imagem,
                on_click=lambda _: get_directory_dialog.get_directory_path(),
                disabled=page.web,
            )
            imagens.controls.append(
                ft.Image(
                    src=imagem,  # Caminho do arquivo,
                    width=300,  # Largura da imagem
                    height=300, # Altura da imagem
                    fit=ft.ImageFit.FILL,  # Ajuste da imagem
                    border_radius=5,
                )
                )
        page.update()'''


    def no_click(j):

        if  j == 0:
            imagem_atual = 0
        else:
            imagem_atual = fotos_path.controls.
        #criar nova linha com o valor do caminho da imagem atual e com isso conseguir usar o index para achar a imagem anterior e posterior
        if j == -1:
            imagem_atual -= 1
        
        if j == 1:
            imagem_atual += 1


        imagem_original.controls.append(
            ft.Image(
                        src=str(fotos_path.controls[imagem_atual]),  # Caminho do arquivo,
                        width=300,  # Largura da imagem
                        height=200, # Altura da imagem
                        fit=ft.ImageFit.FILL,  # Ajuste da imagem
                        border_radius=5,
                    )
            )
        
        page.update()

            


    #variáveis
   
    fotos_path = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
   


    #itens 
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()

    

    imagem_original = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
    imagens = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,     ),
    imagens_pb = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
    imagens_blur = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )
    imagens_hz = Row( alignment=ft.MainAxisAlignment.SPACE_EVENLY,  )


    #linhas 
    linha1 = Row([
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

    linha2 = Row([ 
        ft.Text(value="Escolha a imagem com o melhor contraste:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
    linha3 =  Row( 
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
    
    linha4 = Row([ 
        ft.Text(value="Escolha a imagem com o melhor contraste:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
    linha5 = Row([
        imagens_pb,
    ], 
    spacing=30, 
    alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    linha6 = Row([ 
        ft.Text(value="Escolha a imagem com o melhro blur:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
    linha7 = Row([
        imagens_blur,
    ], 
    spacing=30, 
    alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )
    
    linha8 = Row([ 
        ft.Text(value="Escolha a imagem com a melhor linha horizontal:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
    linha9 = Row([
        imagens_hz

    ], 
    spacing=30, 
    alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    linha10 = Row([ 
        ft.Text(value="Essa é a imagem processada e esses são os valores encontrados:"),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    
    linha11 = Row([
        

    ], 
    spacing=30, 
    alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )
    
    

    
    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])



    page.add(
    
        linha1,
        linha2,
        linha3,
        linha4,
        linha5,
        linha6,
        linha7,
        linha8,
        linha9,
        linha10,
        linha11,
        
    )

ft.app(target=main)

