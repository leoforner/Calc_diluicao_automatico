import flet as ft

def main(page: ft.Page):
    is_web = False  # Variável booleana para desabilitar os botões

    for i in range(5):
        button = ft.ElevatedButton(
            text=f"Botão {i}",
            on_click=lambda e, data=i: print(f"Botão {data} clicado"),
            disabled=is_web
        )
        page.controls.append(button)

    page.update()

ft.app(target=main)