import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Algoritmo para organizar fotos baseado em algum parâmetro do Exif
# Por exemplo: 
# Autor da foto (caso queira separar fotos de vários fotógrafos)
# Copyright (caso queira separar fotos de vários fotógrafos)
# Modelo da câmera (caso fotografe com várias câmeras)
# Modelo da lente (se troca várias vezes de lente)

def exif_to_dict(exif):
    exif_dict = {}
    if exif is not None:
        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            exif_dict[tag_name] = value
    return exif_dict

def read_exif(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            return exif_to_dict(exif_data)
    except (AttributeError, OSError, KeyError, IndexError):
        return None

def organizar_fotos(pasta_origem, pasta_destino):
    for filename in os.listdir(pasta_origem):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Adicione mais extensões, se necessário
            imagem_caminho = os.path.join(pasta_origem, filename)
            autor = read_exif(imagem_caminho)['Artist'] # mude para o parâmetro que quiser, ex: 'Artist' (para autor), 'Model' (modelo da câmera), 'Copyright' ou 'LensModel'

            # Criar pasta para o autor, se ainda não existir
            pasta_autor = os.path.join(pasta_destino, autor)
            os.makedirs(pasta_autor, exist_ok=True)

            # Mover a foto para a pasta do autor
            novo_caminho = os.path.join(pasta_autor, filename)
            os.rename(imagem_caminho, novo_caminho)
            print(f"Foto {filename} movida para {pasta_autor}")

if __name__ == "__main__":
    pasta_origem = 'caminho/das/suas/fotos'
    pasta_destino = 'destino/das/suas/fotos'
    organizar_fotos(pasta_origem, pasta_destino)
    