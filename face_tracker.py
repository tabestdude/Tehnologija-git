import numpy
import cv2

# version 0.5

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # izrežemo iz slike roi, ki smo ga prej izbrali
    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]] 
    cv2.imshow("roi test", roi) 
    # Izracunamo povprecno barvo izbrane slike
    # Dobimo povprecje navpicnih vrstic 
    avg_color_per_col = numpy.mean(roi, axis=1)
    # Preko povprecij navpicnih vrstic nato zracunamo se povprecje vodoravnih vrstic 
    avg_color = numpy.mean(avg_color_per_col, axis=1) 
    # Dodamo šum na min/max vrednost meje koze (+/- 10)
    spodnja_meja_koze = numpy.array((avg_color[0]-10, avg_color[1]-10, avg_color[2]-10))
    zgornja_meja_koze = numpy.array((avg_color[0]+10, avg_color[1]+10, avg_color[2]+10))
    return (spodnja_meja_koze, zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    return numpy.array(cv2.resize(slika, (260, 300)))

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
    resizedImage = zmanjsaj_sliko(image)
    
    # označevanje roi (Region Of Interest), ki se potem uporabi za pridobitev barve kože
    """
    cv2.selectROI() - vrne tuple
       (31, 65, 125, 120)
        ^   ^    ^    ^
        |   |    |    |
        x1  y1   |    y2 = 120 + 65
                x2 = 125 + 31
        x - navzdol // y - vodoravno
        x1,y1 levo zgoraj
        x2,y2 desno spodaj
    """
    if cv2.waitKey(1) == ord('r'):
        roi = cv2.selectROI(resizedImage)
        barva_koze = doloci_barvo_koze(resizedImage, (roi[0], roi[1]), (roi[2] + roi[0], roi[3] + roi[1]))


    # prikaz
    cv2.imshow("\"Face Tracker\"", resizedImage)  

    # QUIT CAPTURE  
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
