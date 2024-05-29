# Bibliotecas
import cv2
import mediapipe as mp

# Configura câmera local
camera = cv2.VideoCapture(0) # O 0 significa a câmera padrão do ambiente

# Inicia as bibliotecas de detecção de gestos
# Será mostrado na tela através de drawing os movimentos captados
mp_hands = mp.solutions.hands
drawing = mp.solutions.drawing_utils

# Inicia modelo de detecção
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:


    # Inicia Câmera
    if not camera.isOpened():
        print("Erro ao abrir a webcam")
        exit()

    while True:
        success, image = camera.read()
        if not success:
            print("Falha ao capturar imagem")
            break
        
        # Aqui começa a detecção de gestos
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        result = hands.process(image)

        # Drawing(Pintura) na tela mostrando resultado
        # Obs o resultado fica na mão mesmo
        # Não descobri uma forma do delay ser menor
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('Webcam', image)
        
        # Dá um 'Close' na câmera após pressionar botão '0'
        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

# Destrói Janela
camera.release()
cv2.destroyAllWindows()
