import os
from PIL import Image

def convert_tiff_to_png(input_file):
    try:
        output_file = os.path.splitext(input_file)[0] + ".png"
        image = Image.open(input_file)
        image.save(output_file, "PNG")
        print("Conversão concluída com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {str(e)}")

# Exemplo de uso
input_file = "F:/backup de arquivos/fotos/IC/imagens-20240604T172236Z-001/Nova pasta/teste2.tif"
convert_tiff_to_png(input_file)

# Print dos metadados antes da conversão
image_before = Image.open(input_file)
print("Metadados antes da conversão:")
print(image_before.info)

# Print dos metadados depois da conversão
output_file = os.path.splitext(input_file)[0] + ".png"
image_after = Image.open(output_file)
print("Metadados depois da conversão:")
print(image_after.info)