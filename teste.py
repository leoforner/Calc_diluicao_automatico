import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
    icons
)
from pathlib import Path

def main(page: ft.Page):
    page.title = "Visualizador de Imagens"



    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"     
        exibir_imagens( directory_path.value)
        directory_path.update()

    


    def exibir_imagens(pasta):
        imagens.controls.clear()
        for arquivo in Path(pasta).iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif"):
                imagens.controls.append(
                    ft.Image(
                        src=str(arquivo),  # Caminho do arquivo,
                        width=300,  # Largura da imagem
                        height=200, # Altura da imagem
                        fit=ft.ImageFit.FILL,  # Ajuste da imagem
                        border_radius=5,
                    )
                )
        page.update()


        # Pasta inicial (pode ser ajustada)
    pasta_inicial = Path.home() / "OneDrive - UFSC/Imagens/Capturas de tela"

    
    imagens = ft.Column( scroll=ft.ScrollMode.ALWAYS, expand=True)
    pasta_selecionada = ft.Text(f"Pasta selecionada: {pasta_inicial}")
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()


    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])


    page.add(
        pasta_selecionada,
        directory_path,
        ft.ElevatedButton(
            "Selecionar Pasta",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=page.web,
        ),
        imagens,
    )

ft.app(target=main)
