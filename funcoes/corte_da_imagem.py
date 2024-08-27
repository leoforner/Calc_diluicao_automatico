import cv2
import os
def crop(input_path, up, bottom, left, right):
    # ler a imagem
    image = cv2.imread(input_path)

    # obter as dimensões da imagem, as variáveis recebidas são as porcentagens de corte
    height, width = image.shape[:2]
    left_slice = width * left
    right_slice = width - (width * right)
    top_slice = height * up
    bottom_slice = height - (height * bottom)

    # cortar a imagem
    cropped_image = image[int(top_slice):int(bottom_slice), int(left_slice):int(right_slice)]

    # criar o diretório "imagens cortadas" a partir do diretório da imagem original
    original_directory = os.path.dirname(input_path)
    cropped_directory = os.path.join(original_directory, "imagens cortadas")
    os.makedirs(cropped_directory, exist_ok=True)

    # salvar a imagem cortada no diretório
    image_name = os.path.basename(input_path)
    cropped_image_path = os.path.join(cropped_directory, image_name)
    cv2.imwrite(cropped_image_path, cropped_image)

    return cropped_image_path

# Exemplo de uso
input_path = 'imagens de exemplo/teste.tif'
output = crop(input_path, 0.2, 0.2, 0.2, 0.2)
