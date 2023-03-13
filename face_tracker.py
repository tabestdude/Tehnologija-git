import numpy as np
import cv2 as cv

# version 0.1

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    pass
    return (spodnja_meja_koze,zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    pass

def obdelaj_sliko(slika, okno_sirina, okno_visina,barva_koze_spodaj, barva_koze_zgoraj):
    pass

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    pass

cap = cv.VideoCapture(0)
ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,260)
ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT,300)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
