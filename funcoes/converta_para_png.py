from todas_bibliotecas_e_funcoes import *


def convert_tiff_to_png(input_file):
    try:
        # Cria a pasta de saída para armazenar as imagens PNG
        output_folder = os.path.join(os.path.dirname(input_file), "png")
        os.makedirs(output_folder, exist_ok=True)
        
        # Define o caminho e o nome do arquivo de saída em formato PNG
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".png")
        
        # Abre a imagem TIFF de entrada
        image = Image.open(input_file)
        
        # Salva a imagem no formato PNG no arquivo de saída
        image.save(output_file, "PNG")
        
        # Imprime uma mensagem de sucesso
        print("Conversão concluída com sucesso!")
    except Exception as e:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Ocorreu um erro durante a conversão: {str(e)}")

# Exemplo de uso
input_file = 'imagens de exemplo/teste.tif'
convert_tiff_to_png(input_file)

