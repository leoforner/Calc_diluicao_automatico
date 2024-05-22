
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
    )

ft.app(target=main)



'''

import flet as ft
import os

def main(page: ft.Page):
    page.title = "Image Viewer"

    def open_folder(e):

        file_picker = ft.FilePicker()
        folder_path = file_picker.get_directory_path()
        if folder_path:
            display_images(folder_path)

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

        page.controls.clear()
        for i, image in enumerate(images):
            image.on_click = lambda e, image=image: open_image(e, image)
            page.controls.append(image)
            if (i + 1) % 5 == 0:
                page.controls.append(ft.Divider())
        page.update()

    
    page.add(
        ft.ElevatedButton("Select Folder", on_click=open_folder),
        ft.Row([ft.Text("Press ESC to exit full-screen image")]),
    )

ft.app(target=main, upload_dir="uploads")

'''

'''
# FUNCIONANDO

import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


def main(page: Page):
    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    # Save file dialog
    def save_file_result(e: FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Cancelled!"
        save_file_path.update()

    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, save_file_dialog, get_directory_dialog])

    page.add(
        Row(
            [
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                selected_files,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Save file",
                    icon=icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(),
                    disabled=page.web,
                ),
                save_file_path,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ]
        ),
    )


flet.app(target=main)

'''