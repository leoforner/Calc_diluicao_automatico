from funcoes.funcoes import *
from funcoes.bibliotecas import *

# Função para converter um array NumPy em uma imagem base64 PNG
def numpy_to_base64(np_array):
    image = Image.fromarray(np_array.astype('uint8'))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Função para redimensionar uma imagem mantendo a proporção
    
def proportional_scale(image, scale_factor):
    height, width = image.shape[:2]
    proportion = width / height
    screen_width, screen_height = pyautogui.size()
    new_height = int(screen_height * scale_factor)
    new_width = int(new_height * proportion)
    
    return new_width, new_height


def main(page: ft.Page):
    '''# funções das principais variaveis 
    
    
    '''
    
    
    # Definir variáveis para a página
    page.title = "Cálculo de Diluição"
    page.scroll = True
    is_web = False  # Variável booleana para desabilitar botões

    # Variável para controlar a visibilidade
    is_visible = ft.Ref[bool]()
    is_visible.value = False

    # Variáveis para controlar a largura e altura das imagens
    global big_width, big_height, small_width, small_height
    big_width=300
    big_height=300
    small_width=150
    small_height=150    


    # Armazenamento de dados
    directory_path = ft.Text(data=[])  # Caminho do diretório selecionado pelo usuário
    original_image = Container(
        image_src='imagens_exemplo/teste.tif',
        width=  big_width,
        height=  big_height, 
        image_fit=ft.ImageFit.FILL, 
        data=0,
    )
    bw_images = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])  # Imagens em escala de cinza
    blur_images = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])  # Imagens com desfoque
    edges_images = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])  # Imagens com detecção de bordas
    horizontal_images = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])  # Imagens com linhas horizontais
    final_image = Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, data=[0, 0, 0, 0, 0])  # Imagem final processada

    
    def update_dimensions(image):
        global big_width, big_height, small_width, small_height
        
        big_width, big_height = proportional_scale(image, 0.5)
        small_width, small_height = proportional_scale(image, 0.2)
        
        original_image.width = big_width
        original_image.height = big_height  



    # Manipuladores de eventos

    # Manipulador de evento para obter o diretório selecionado pelo usuário
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelado!"
        directory_path.data.clear()
        for file in Path(directory_path.value).iterdir():
            if file.is_file() and file.suffix.lower() in (".jpg", ".jpeg", ".png", '.tif'):
                
                # Exibir os elementos da página
                is_visible.value = True
                Folder_Selection.visible = is_visible.value
                current.visible = is_visible.value
                blur.visible = is_visible.value
                bw.visible = is_visible.value
                horizontal.visible = is_visible.value
                final.visible = is_visible.value



                new_path = str(file).replace("\\", "/")
                directory_path.data.append(new_path)

        #dimensões da imagem
        image = cv2.imread( directory_path.data[0])
        update_dimensions(image)
        


        original_image.data = 0
        original_image.image_src = directory_path.data[original_image.data]
        original_image.update()
        current.update()
        process_blur()


    # Manipulador de evento para exibir a próxima imagem
    def next_image(e):
        if original_image.data == len(directory_path.data) - 1:
            original_image.data = 0
        else:
            original_image.data += 1


        #dimensões da imagem
        image = cv2.imread( directory_path.data[original_image.data])
        update_dimensions(image)


        original_image.image_src = directory_path.data[original_image.data]
        original_image.update()
        current.update()
        process_blur()

    # Manipulador de evento para exibir a imagem anterior
    def previous_image(e):
        if original_image.data == 0:
            original_image.data = len(directory_path.data) - 1
        else:
            original_image.data -= 1


        #dimensões da imagem
        image = cv2.imread( directory_path.data[original_image.data])
        update_dimensions(image)


        original_image.image_src = directory_path.data[original_image.data]
        original_image.update()
        current.update()
        process_blur()


    # Função para processar as imagens com desfoque
    def process_blur():
        blur_images.controls.clear()
        crop_image = crop(original_image.image_src, 0.01, 0.1, 0.01, 0.01)
        image = Image.open(crop_image).convert('RGB')
        
        image = np.array(image)
        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        items = []

        for i in range(5):
            BLUR = cv2.GaussianBlur(bw_image, (1 + i*20, 1 + i*20), 0)
            blur_images.data[i] = BLUR
            base64_image = numpy_to_base64(BLUR)

            items.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=small_width,
                        height=small_height,
                    ),
                    ft.ElevatedButton(
                        text=f"Botão {i}",
                        on_click=lambda e, data=i: process_bw(blur_images.data[data]),
                        disabled=is_web,
                    ),
                ])
            )

        blur_images.controls = items
        blur_images.update()
        blur.update()
        process_bw(blur_images.data[0])

    # Função para processar as imagens em escala de cinza
    def process_bw(ima):
        bw_images.controls.clear()
        items = []

        for i in range(5):
            ret,thresh = cv2.threshold(ima,(1 + (15*i)),255,0)
            bw_images.data[i] = thresh
            base64_image = numpy_to_base64(thresh)

            items.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=small_width,
                        height=small_height,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        on_click=lambda e, data=i: process_edges(bw_images.data[data]),
                        disabled=is_web,
                    ),
                ])
            )

        bw_images.controls = items
        bw_images.update()
        bw.update()
        process_edges(bw_images.data[0])

    # Função para processar as imagens com detecção de bordas
    def process_edges(image):
        edges_images.controls.clear()
        items = []

        for i in range(5):
            edges = cv2.Canny(image, i*10+30, i*10+130)
            edges_images.data[i] = edges
            base64_image = numpy_to_base64(edges)

            items.append(
                ft.Column([
                    ft.Image(
                        src_base64=base64_image,
                        width=small_width,
                        height=small_height,
                    ),
                    ft.ElevatedButton(
                        f"Imagem {i}",
                        on_click=lambda e, data=i: process_horizontal(edges_images.data[data]),
                        disabled=is_web,
                    ),
                ])
            )

        edges_images.controls = items
        edges_images.update()
        horizontal.update()
        process_horizontal(edges_images.data[0])

    # Função para processar as imagens com linhas horizontais
    def process_horizontal(edges):
        if original_image.image_src != None:
            image = cv2.imread(original_image.image_src)
        else:
            image = cv2.imread("C:/Users/leona/OneDrive - UFSC/Images/robota/Caputinho.png")
        images = []
        horizontal_images.controls.clear()
        items = []

        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=500, maxLineGap=1000)
        if lines is None:
            pass
        else:

            sorted_lines = sorted(lines, key=lambda line: line[0][2] - line[0][0], reverse=True)
            top_lines = sorted_lines[:5]

            for i in range(len(top_lines)):
                images.append(image.copy())

                x1, y1, x2, y2 = top_lines[i][0]
                cv2.line(images[i], (x1, y1), (x2, y2), (255, 0, 0), 25)

                horizontal_images.data[i] = images[i]
                base64_image = numpy_to_base64(images[i])

                items.append(
                    ft.Column([
                        ft.Image(
                            src_base64=base64_image,
                            width=small_width,
                            height=small_height,
                        ),
                        ft.ElevatedButton(
                            f"Imagem {i}",
                            on_click=lambda e, data=i: process_final_image(horizontal_images.data[data]),
                            disabled=is_web,
                        ),
                    ])
                )

        horizontal_images.controls = items
        horizontal_images.update()
        horizontal.update()
        final.update()
        process_final_image(horizontal_images.data[0])

    # Função para exibir a imagem final processada
    def process_final_image(ima):
        final_image.controls.clear()
        items = []

        if ima == None:
            ima = Image.open(original_image.image_src).convert('RGB')
        
            ima = np.array(image)
            

        base64_image = numpy_to_base64(ima)

        items.append(
            ft.Column([
                ft.Image(
                    src_base64=base64_image,
                    width=big_width,
                    height=big_height,
                ),
            ])
        )

        final_image.controls = items
        final_image.update()
        final.update()
        page.update()

    # Elementos de UI
    get_directory_dialog = FilePicker(on_result=get_directory_result)

    Folder_Selection = Row([
        ft.Text(value="Escolha a pasta que deseja analisar:"),
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

    current = Column(
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
                    "Imagem Anterior",
                    icon=icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                    on_click=previous_image,
                    disabled=is_web,
                ),
                original_image,
                ft.ElevatedButton(
                    "Próxima Imagem",
                    icon=icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
                    on_click=next_image,
                    disabled=is_web,
                ),
                ],
                spacing=30,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    blur = Column([
        ft.Text(value="Escolha a imagem com o melhor desfoque:"),
        blur_images,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    bw = Column([
        ft.Text(value="Escolha a imagem com o melhor contraste:"),
        bw_images,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    horizontal = Column([
        ft.Text(value="Escolha a imagem com a melhor detecção de borda:"),
        edges_images,
        ft.Text(value="Escolha a imagem com a melhor linha horizontal:"),
        horizontal_images,
    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    final = Row([
        ft.Text(value="Esta é a imagem processada e estes são os valores encontrados:"),
        final_image,

    ],
    spacing=30,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    # Configuração da visibilidade dos elementos
    current.visible = is_visible.value
    blur.visible = is_visible.value
    bw.visible = is_visible.value
    horizontal.visible = is_visible.value
    final.visible = is_visible.value


    # Configuração da página
    page.overlay.extend([get_directory_dialog])
    page.add(
        Folder_Selection,
        current,
        blur,
        bw,
        horizontal,
        final,
    )

ft.app(target=main)