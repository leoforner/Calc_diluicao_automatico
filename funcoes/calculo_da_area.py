from funcoes.funcoes import *
from funcoes.bibliotecas import *


def calculate_area(path, comprimento_real_mm):
    # função para calcular a qunatidade de pixels por mm
    pixes_per_mm = calculate_pixels_per_mm(comprimento_real_mm, path, 0.75)
    
    def grafico(img):
        # Definindo o tamanho da janela
        cv2.namedWindow("Starting image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Starting image", 800, 600)
        cv2.imshow("Starting image", img)
        cv2.waitKey()

    path = crop(path, 0, 0.1, 0.1, 0.1)

    # sourcing the input image
    img = cv2.imread(path)
    grafico(img)


    # Convertendo para escala de cinza
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grafico(imgGray)

    # Aplicando Canny edge detection
    imgCanny = cv2.Canny(imgGray, 255, 15)
    grafico(imgCanny)

    # Dilatando a imagem
    kernel = np.ones((2, 2))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=3)
    grafico(imgDil)

    # Erodindo a imagem
    imgThre = cv2.erode(imgDil, kernel, iterations=3)
    grafico(imgThre)

    # Encontrando contornos
    contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrando contornos
    finalContours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            finalContours.append(cnt)

    # Desenhando contornos na imagem
    imgContour = img.copy()
    cv2.drawContours(imgContour, finalContours, -1, (0, 0, 255), 3)

    # Calculando a área do objeto em pixels
    objectPixelArea = cv2.contourArea(finalContours[0])

    # Calculando a área do objeto em mm^2
    objectArea = objectPixelArea/ pixes_per_mm

    print("Área do objeto em mm^2:", objectArea)

    # Mostrando a imagem com os contornos
    grafico(imgContour)

    cv2.destroyAllWindows()

'''
# Example usage
calculate_area('imagens de exemplo/teste1.tif', 1)
'''