from todas_bibliotecas_e_funcoes import *

def remover_fundo(input_path):

    # remover background da imagem
    input = cv2.imread(input_path)
    output = remove(input)
 
    # criar o diretório "sem_fundo" a partir do diretório da imagem original
    original_directory = os.path.dirname(input_path)
    rembg_directory = os.path.join(original_directory, "sem_fundo")
    os.makedirs(rembg_directory, exist_ok=True)

    # salvar a imagem sem fundo no diretório
    image_name = os.path.basename(input_path)
    rembg_image_path = os.path.join(rembg_directory, image_name)
    cv2.imwrite(rembg_image_path, output)

    return rembg_image_path

    

# Exemplo de uso da função
remover_fundo("imagens de exemplo/teste.tif")