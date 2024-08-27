import cv2

def corte(imagem,cima,baixo,esquerda,direita):
    # obter dimensões da imagem
    altura, largura = imagem.shape[:2]
    corte_esquerda = largura*esquerda
    corte_direita = largura-(largura*direita)
    corte_cima = altura*cima
    corte_baixo = altura-(altura*baixo)

    # cortar a imagem
    imagem_cortada = imagem[int(corte_cima):int(corte_baixo), int(corte_esquerda):int(corte_direita)]

    return imagem_cortada

# Store path of the image in the variable input_path 
input_path = 'F:/backup de arquivos/fotos/IC/Nova pasta/teste3.png' 

# Store path of the output image in the variable output_path 
output_path = 'F:/backup de arquivos/fotos/IC/Nova pasta/teste3b2g.png' 


input = cv2.imread(input_path)
output = corte(input,0.2,0.2,0.2,0.2)#remove(input)
cv2.imwrite(output_path, output) # type: ignore