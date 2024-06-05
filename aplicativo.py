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
                fotos_path.append(arquivo)


        #exibir_imagens( directory_path.value)
        directory_path.update()

    
    def exibir_imagens(versoes):
        
        imagens.controls.clear()
        for imagem in versoes: 
            imagens.controls.append(
                ft.Image(
                    src=imagem,  # Caminho do arquivo,
                    width=300,  # Largura da imagem
                    height=300, # Altura da imagem
                    fit=ft.ImageFit.FILL,  # Ajuste da imagem
                    border_radius=5,
                )
                )
        page.update()



    # a função escolha_pb() receberá uma imagem  e a partir dela criará 5 versóes da foto e as exibirá
    
    
    imagens = ft.Column( scroll=ft.ScrollMode.ALWAYS, expand=True)
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()
    fotos_path = []


    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])

    #Fotos_pb = escolha_pb()
    


    page.add(
        Row(
        [
            ft.ElevatedButton(
                "Selecionar Pasta",
                icon=icons.FOLDER_OPEN,
                on_click=lambda _: get_directory_dialog.get_directory_path(),
                disabled=page.web,
            ),
            directory_path,
            imagens,
            #Fotos_pb,
        ],D
        spacing=30,
        alignment=ft.MainAxisAlignment.START,
        ),
       
     imagens,
        
    )

ft.app(target=main)

