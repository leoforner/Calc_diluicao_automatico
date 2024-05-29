import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
)
from pathlib import Path

def main(page: ft.Page):
    page.title = "Visualizador de Imagens"



    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
    
        pasta_inicial = directory_path.value

    


    def exibir_imagens(pasta):
        imagens.controls.clear()
        for arquivo in pasta.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif"):
                imagens.controls.append(
                    ft.Image(
                        src=arquivo,
                        width=300,  # Largura da imagem
                        height=200, # Altura da imagem
                        fit="ImageFit",  # Ajuste da imagem
                        border_radius=5,
                    )
                )
        page.update()


        # Pasta inicial (pode ser ajustada)
    pasta_inicial = Path.home() / "Imagens"

    imagens = ft.Column(scroll="ScrollMode")
    pasta_selecionada = ft.Text(f"Pasta selecionada: {pasta_inicial}")
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()


    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])


    page.add(
        pasta_selecionada,
        directory_path,
        ft.ElevatedButton("Selecionar Pasta", on_click=get_directory_dialog.get_directory_path()),
        
        imagens,
    )

    # Exibir imagens da pasta inicial ao iniciar
    exibir_imagens(pasta_inicial)

ft.app(target=main)
