import os
import sys
import cv2
import base64
import numpy as np


def base64_to_image(base64_string):
    """Converte base64 para imagem (OpenCV)."""
    img_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def image_to_base64(img):
    """Converte imagem (OpenCV) para base64."""
    _, buffer = cv2.imencode('.jpg', img)
    base64_str = base64.b64encode(buffer).decode('utf-8')
    return base64_str


def recortar_e_zoom_no_rosto(imagem_base64, fator_zoom=1.5):
    """Recorta a imagem para dar um zoom no rosto, mantendo a proporção 16:9."""
    img = base64_to_image(imagem_base64)

    # Determina o caminho do classificador
    base_path = os.path.dirname(
        os.path.abspath(__file__))  # Diretório do script
    face_cascade = cv2.CascadeClassifier(os.path.join(
        base_path, 'haarcascade_frontalface_default.xml'))

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta rostos
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise Exception("Nenhum rosto encontrado na imagem.")

    x, y, w, h = faces[0]
    centro_x = x + w // 2
    centro_y = y + h // 2

    novo_h = int(h * fator_zoom)
    novo_w = int(novo_h * 16 / 9)

    novo_x = max(0, centro_x - novo_w // 2)
    novo_y = max(0, centro_y - novo_h // 2)

    novo_x = min(novo_x, img.shape[1] - novo_w)
    novo_y = min(novo_y, img.shape[0] - novo_h)

    rosto_zoomado = img[novo_y:novo_y + novo_h, novo_x:novo_x + novo_w]

    return rosto_zoomado, image_to_base64(rosto_zoomado)


# Função principal
if __name__ == "__main__":
    base64_string = sys.argv[1]  # Recebe o argumento do bash

    try:
        imagem_zoomada, imagem_base64_resultante = recortar_e_zoom_no_rosto(
            base64_string)

        # Salva a imagem resultante como .jpg
        nome_imagem_saida = "resultado_zoomado.jpg"
        cv2.imwrite(nome_imagem_saida, imagem_zoomada)

        # Salva a imagem resultante em base64 no arquivo .txt
        nome_base64_saida = "resultado_base64.txt"
        with open(nome_base64_saida, "w") as f:
            f.write(imagem_base64_resultante)

        print(
            f"Imagem zoomada salva como '{nome_imagem_saida}' e '{nome_base64_saida}'.")
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
