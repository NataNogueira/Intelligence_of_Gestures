# Biblioteca usada
import cv2

# Inicializa a captura de vídeo para a webcam do meu notebook
capture = cv2.VideoCapture(0)

while(True):
    # Captura quadro por quadro
    ret, frame = capture.read()

    # Exibe o quadro resultante
    cv2.imshow('Webcam em tempo real', frame)

    # Se 'q' for pressionado no teclado, o loop será interrompido, lembrando q não tem como fechar no x 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Após apertar 'q' destrói a janela
capture.release()
cv2.destroyAllWindows()
