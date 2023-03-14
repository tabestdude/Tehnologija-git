import numpy
import cv2

# version 0.4

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    return (spodnja_meja_koze, zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    pass

def obdelaj_sliko(slika, okno_sirina, okno_visina, barva_koze_spodaj, barva_koze_zgoraj):
    pass

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    pass


# ZACETEK PROGRAMA
         
# Zajem kamere
cap = cv2.VideoCapture(0)

# Preverjanje ce se je kamero dalo odpret
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
barva_koze = None
while True:    

    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    # preslikava posnetka kamere (1 slika) v numpy.array()
    image = numpy.array(frame)
    
    # označevanje roi (Region Of Interest), ki se potem uporabi za pridobitev barve kože
    if cv2.waitKey(1) == ord('r'):
        roi = cv2.selectROI(frame)

    # prikaz
    cv2.imshow("\"Face Tracker\"", frame)  

    # QUIT CAPTURE  
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
