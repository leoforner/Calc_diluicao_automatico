
import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
import os

def main(page: Page):

    page.title = "Image Viewer"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.update()

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()
  
        images = [
            #ft.Image(src=os.path.join(directory_path, image_file))
            #for image_file in os.listdir(directory_path)
            #if image_file.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        # Create a list to store the file names
        #file_names = []

        # Iterate over the selected files and add their names to the list
        #for file in enumerate(selected_files):
        #    file_names.append(file.name)

        # Create a Text object to display the file names
        #file_names_text = Text(value="\n".join(file_names))

        # Add the Text object to the page
        #page.add(file_names_text)

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()
    selected_files = Text()

    '''
        def display_images(folder_path):
            images = [
                ft.Image(src=os.path.join(folder_path, image_file))
                for image_file in os.listdir(folder_path)
                if image_file.lower().endswith((".png", ".jpg", ".jpeg"))
            ]

            def open_image(e, image):
                def close_image(e):
                    page.controls.remove(image_view)
                    page.update()

                image_view = ft.Image(
                    src=image.src,
                    width=page.width,
                    height=page.height,
                    on_click=close_image
                )
                page.controls.append(image_view)
                page.update()

                #page.controls.clear()
                for i, image in enumerate(images):
                    image.on_click = lambda e, image=image: open_image(e, image)
                    page.controls.append(image)
                    if (i + 1) % 5 == 0:
                        page.controls.append(ft.Divider())
                page.update()
        '''



    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])

    page.add(
           Row(
            [
                ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
                selected_files,
            ]
        ),
        Row(
            [
                Text(
                    "Press ESC to exit full-screen image"
                )
            ]
        ),
        Row(
            [
                
            ]
        ),
    )

ft.app(target=main)
