import cv2
import base64
import numpy as np
import sys
import os


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

    # Determina o caminho do classificador Haarcascade
    haarcascade_path = os.path.join(os.path.dirname(
        __file__), 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(haarcascade_path)

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta rostos
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Verifica se encontrou algum rosto
    if len(faces) == 0:
        raise Exception("Nenhum rosto encontrado na imagem.")

    # Para o primeiro rosto detectado, calcula o recorte
    x, y, w, h = faces[0]
    centro_x = x + w // 2
    centro_y = y + h // 2

    # Calcula as novas dimensões do recorte para 16:9
    novo_h = int(h * fator_zoom)
    novo_w = int(novo_h * 16 / 9)  # Proporção 16:9

    # Calcula as coordenadas do recorte
    novo_x = max(0, centro_x - novo_w // 2)
    novo_y = max(0, centro_y - novo_h // 2)

    # Garante que o recorte não saia das bordas da imagem
    novo_x = min(novo_x, img.shape[1] - novo_w)
    novo_y = min(novo_y, img.shape[0] - novo_h)

    # Recorta a imagem
    rosto_zoomado = img[novo_y:novo_y + novo_h, novo_x:novo_x + novo_w]

    # Redimensiona a imagem zoomada para 16:9, mantendo a proporção
    imagem_final = cv2.resize(rosto_zoomado, (novo_w, novo_h))

    return image_to_base64(imagem_final)


if __name__ == "__main__":
    try:
        # Verifica se o argumento foi passado
        if len(sys.argv) < 2:
            raise Exception("É necessário passar o base64 como argumento.")

        # Lê o base64 do argumento
        imagem_base64 = sys.argv[1].strip()

        # Recorta a imagem para dar zoom no rosto e obtém a imagem em base64
        imagem_base64_resultante = recortar_e_zoom_no_rosto(imagem_base64)

        # Imprime o resultado base64
        print(imagem_base64_resultante)

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
