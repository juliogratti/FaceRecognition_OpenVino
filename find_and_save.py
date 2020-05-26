import sys
import threading
import cv2

# ==========================================
class WebcamError(ValueError):
    pass

# ==========================================
class WebcamCap(threading.Thread):

    # --------------------------------------
    def __init__(self, webcam = 0):
        super().__init__(None, self)

        self._webcam = webcam
        '''Id da Webcam a ser utilizada. O default é 0 (principal).'''

        self._video = cv2.VideoCapture(self._webcam)
        '''Objeto para captura do vídeo.'''

        if not self._video.isOpened():
            raise WebcamError('Não foi possível iniciar a Webcam.')

        self._lock = threading.Lock()
        '''Mutex usado para a sincronização entre as threads.'''

        self._frames = []
        '''Lista de quadros capturados e aptos a serem processados.'''

        self._started = threading.Event()
        '''Evento usado para controlar a inicialização da câmera.'''

        self._running = False
        '''Flag usada para indicar e controlar se a Thread está em execução.'''

    # --------------------------------------
    def __del__(self):
        self._video.release()

    # --------------------------------------
    def start(self):
        if not self.isRunning():
            super().start()
            # Aguarda até que a câmera seja inicializada corretamente
            self._started.clear()
            self._started.wait()

    # --------------------------------------
    def stop(self):
        self._lock.acquire()
        self._running = False
        self._lock.release()

    # --------------------------------------
    def isRunning(self):
        self._lock.acquire()
        ret = self._running
        self._lock.release()
        return ret

    # --------------------------------------
    def pop(self):
        self._lock.acquire()
        try:
            frame = self._frames.pop()
        except:
            frame = None
        self._lock.release()
        return frame

    # --------------------------------------
    def run(self):
        # Força a leitura do primeiro quadro, já que a inicialização da câmera
        # demora um pouco
        ret, frame = self._video.read()
        if ret:
            self._frames.append(frame)
            self._running = True
            self._started.set() # Evento indicando a inicialização
        else:
            raise WebcamError('Não foi possível acessar a Webcam.')

        # Loop principal de leitura
        while self.isRunning():
            ret, frame = self._video.read()
            if ret:
                self._lock.acquire()
                self._frames.append(frame)
                self._lock.release()

# ==========================================
def webvideo(path):

    fps = 20 # Taxa de reprodução (em quadros por segundo)
    delay = int(1 / fps * 1000) # Tempo de 1 quadro em milisegundos

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path, fourcc, fps, (640,480))

    try:
        cam = WebcamCap()
    except WebcamError as e:
        print(e.message)
        sys.exit(-1)

    cam.start()
    while True:

        frame = cam.pop()
        if frame is not None:
            out.write(frame)

            cv2.imshow('Webcam', frame)

            if cv2.waitKey(delay) == ord('q'):
                break
        else:
            print('Erro capturando video da Webcam')
            break

    cam.stop()
    out.release()

webvideo('teste.avi')
























#import cv2


#cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

#while(cap.isOpened()):
#    ret, frame = cap.read()
#    if ret==True:
#        out.write(frame)

 #       cv2.imshow('frame',frame)
 #       if cv2.waitKey(1) & 0xFF == ord('q'):
 #           break
#    else:
#        break

#cap.release()
#out.release()
