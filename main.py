# Bibliotecas
import cv2
import mediapipe as mp

# Configura câmera local
camera = cv2.VideoCapture(0) # O 0 significa a câmera padrão do ambiente

# Inicia as bibliotecas de detecção de gestos
# Será mostrado na tela através de drawing os movimentos captados
mp_hands = mp.solutions.hands
drawing = mp.solutions.drawing_utils

def reconhecer_gestos(hand_landmarks):
    polegar_para_cima = False
    mao_aberta = False

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if thumb_tip.y < wrist.y and index_finger_tip.y > wrist.y:
        polegar_para_cima = True

    if (thumb_tip.x < index_finger_tip.x < middle_finger_tip.x < ring_finger_tip.x < pinky_tip.x) and \
       (thumb_tip.y < wrist.y and index_finger_tip.y < wrist.y and middle_finger_tip.y < wrist.y and ring_finger_tip.y < wrist.y and pinky_tip.y < wrist.y):
        mao_aberta = True

    return polegar_para_cima, mao_aberta

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
                polegar_para_cima, mao_aberta = reconhecer_gestos(hand_landmarks)
                if polegar_para_cima:
                    cv2.putText(image, 'Polegar para Cima', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                elif mao_aberta:
                    cv2.putText(image, 'Mao Aberta', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Webcam', image)

        # Dá um 'Close' na câmera após pressionar botão '0'
        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

# Destrói Janela
camera.release()
cv2.destroyAllWindows()
