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


def desenhar_circulo_no_rosto(imagem_base64):
    """Desenha um círculo ao redor do rosto detectado na imagem."""
    img = base64_to_image(imagem_base64)

    # Carrega o classificador pré-treinado para detecção de rostos
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

    # Desenha um círculo ao redor do rosto
    for (x, y, w, h) in faces:
        centro_x = x + w // 2
        centro_y = y + h // 2
        raio = int((w + h) / 4)  # Raio médio do círculo
        cv2.circle(img, (centro_x, centro_y), raio,
                   (0, 255, 0), 2)  # Verde, espessura 2

    return img, image_to_base64(img)


# Função principal para processar múltiplos arquivos
if __name__ == "__main__":
    arquivos_base64 = ["base1.txt", "base2.txt", "base3.txt", "base4.txt"]

    for arquivo in arquivos_base64:
        try:
            # Lê a imagem base64 do arquivo
            with open(arquivo, "r") as f:
                imagem_base64 = f.read()

            # Desenha o círculo no rosto e obtém a imagem e base64
            imagem_com_circulo, imagem_base64_resultante = desenhar_circulo_no_rosto(
                imagem_base64)

            # Salva a imagem resultante como .jpg
            nome_imagem_saida = arquivo.replace('.txt', '_com_circulo.jpg')
            cv2.imwrite(nome_imagem_saida, imagem_com_circulo)

            # Salva a imagem resultante em base64 no arquivo .txt
            nome_base64_saida = arquivo.replace('.txt', '_base64.txt')
            with open(nome_base64_saida, "w") as f:
                f.write(imagem_base64_resultante)

            print(
                f"Imagem com círculo ao redor do rosto salva como '{nome_imagem_saida}' e '{nome_base64_saida}'.")
        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")
