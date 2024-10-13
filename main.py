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


def detectar_rosto(imagem_base64):
    """Detecta o rosto na imagem e retorna o rosto em OpenCV e base64."""
    img = base64_to_image(imagem_base64)

    # Carrega o classificador pré-treinado
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecta rostos
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Verifica se encontrou algum rosto
    if len(faces) == 0:
        raise Exception("Nenhum rosto encontrado na imagem.")

    # Recorta o primeiro rosto encontrado
    x, y, w, h = faces[0]
    rosto = img[y:y+h, x:x+w]

    # Retorna o rosto como imagem OpenCV e em base64
    return rosto, image_to_base64(rosto)


# Exemplo de uso
if __name__ == "__main__":
    try:
        # Lê a imagem base64 de um arquivo
        with open("exemplo_base64.txt", "r") as f:
            imagem_base64 = f.read()

        # Detecta o rosto e obtém a imagem e base64
        rosto_img, rosto_base64 = detectar_rosto(imagem_base64)

        # Salva o rosto em base64 no arquivo .txt
        with open("rosto_base64.txt", "w") as f:
            f.write(rosto_base64)

        # Salva o rosto como uma imagem .jpg
        cv2.imwrite("rosto.jpg", rosto_img)

        print("Imagem do rosto salva em 'rosto.jpg' e 'rosto_base64.txt'.")
    except Exception as e:
        print(f"Erro: {e}")
