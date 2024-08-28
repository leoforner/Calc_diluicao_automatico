import cv2
import numpy as np
from corte_da_imagem import crop

import matplotlib.pyplot as plt

def calculate_pixels_per_mm(real_length_mm, image_path, crop_percentage):

    # Carrega a imagem
    image_path = crop(image_path, crop_percentage, 0, crop_percentage, 0)
    image = cv2.imread(image_path)

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica a detecção de bordas
    edges = cv2.Canny(gray, 50, 150)

    # Detecta linhas usando a transformada de Hough
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

    # Calcula o comprimento de cada linha
    line_lengths = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        line_lengths.append(length)

    # Encontra o índice da linha mais longa
    max_length_index = np.argmax(line_lengths)

    # Obtém as coordenadas da linha mais longa
    x1, y1, x2, y2 = lines[max_length_index][0]

    # Calcula o comprimento da linha mais longa
    max_length = line_lengths[max_length_index]

    # Calcula pixels por mm
    pixels_per_mm = max_length / real_length_mm
    
    '''
    # Desenha a linha mais longa na imagem
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Mostra a imagem com a linha mais longa
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
    '''


    return pixels_per_mm

# Exemplo de uso
real_length_mm = 1
image_path = 'imagens de exemplo/teste1.tif'
crop_percentage = 0.75

pixels_per_mm = calculate_pixels_per_mm(real_length_mm, image_path, crop_percentage)
print("Pixels por mm:", pixels_per_mm)
