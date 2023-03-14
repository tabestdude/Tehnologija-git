import numpy
import cv2

# version 1.0

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # Izrežemo iz slike roi, ki smo ga prej izbrali
    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]] 
    # Izracunamo povprecno barvo izbrane slike
    # Dobimo povprecje vodoravnih vrstic 
    avg_color_row= numpy.mean(roi, axis=0)
    # Preko povprecij navpicnih vrstic nato zracunamo se povprecje navpicnih vrstic 
    avg_color = numpy.mean(avg_color_row, axis=0) 
    # Dodamo šum na zgornjo/spodnjo vrednost meje koze (+/- 15)
    spodnja_meja_koze = numpy.array((avg_color[0]-15, avg_color[1]-15, avg_color[2]-15))
    zgornja_meja_koze = numpy.array((avg_color[0]+15, avg_color[1]+15, avg_color[2]+15))
    return (spodnja_meja_koze, zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    # cv2.resize() spremeni velikost slike // numpy.array() pa to sliko pretvori v tip numpy.array()
    return numpy.array(cv2.resize(slika, (260, 300)))

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    # cv2.inRange() vrne 0 če ni v tistem intervalu
    skinColorRange = cv2.inRange(podslika, barva_koze_spodaj, barva_koze_zgoraj)
    skinCounter = cv2.countNonZero(skinColorRange)
    return skinCounter

def obdelaj_sliko(slika, okno_sirina, okno_visina, barva_koze_spodaj, barva_koze_zgoraj):
    # Dobimo skatlo s katero bomo shranjevali na katerem mestu se je pojavilo ujemanje 
    # povprecja z intervalu zgornje/spodnje meje
    roiBox_width = int(slika.shape[1] * okno_sirina / 100)
    roiBox_height = int(slika.shape[0] * okno_visina / 100)
    matchSkinBox = None
    # Skatlo premikamo po celi sliki in ji poiscemo povprecno vrednost
    # Povprecna vrednost skatle primerjamo, ce je na intervalu zgornje/spodnje meje
    for x in range(0, slika.shape[1] - roiBox_width, roiBox_width):
        for y in range(0, slika.shape[0] - roiBox_height, roiBox_height):
            movingBox = resizedImage[y:y+roiBox_height, x:x+roiBox_width]
            avg_color_per_row = numpy.mean(movingBox, axis=0)
            avg_color = numpy.mean(avg_color_per_row, axis=0)
            # Prestejemo piksle, ki so v intervalu spodnje/zgornje meje
            skinCounter = prestej_piksle_z_barvo_koze(movingBox, barva_koze[0], barva_koze[1])
            print("Piksli kozne barve :", skinCounter)

            if (avg_color >= barva_koze_spodaj).all() and (avg_color <= barva_koze_zgoraj).all():
                # Povprečna vrednost piksla te 'skatle' se ujema z povprecno vrednostjo koze in si jo shranimo
                matchSkinBox = (x, y, x+roiBox_width, y+roiBox_height)
                break
        if matchSkinBox is not None:
            break
    return matchSkinBox


# --- ZACETEK PROGRAMA ---
         
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

    # Preslikava posnetka kamere (1 slika) v numpy.array()
    image = numpy.array(frame)
    resizedImage = zmanjsaj_sliko(image)
    
    # Označevanje roi (Region Of Interest), ki se potem uporabi za pridobitev barve kože
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

    okno_visina = 15
    okno_sirina = 15
    if barva_koze != None:
        skinMatchBox = obdelaj_sliko(resizedImage, okno_sirina, okno_visina, barva_koze[0], barva_koze[1])
        if skinMatchBox != None:
            cv2.rectangle(resizedImage, (skinMatchBox[0], skinMatchBox[1]), (skinMatchBox[2], skinMatchBox[3]), (0, 255, 0), 2)

    # Prikaz obdelane slike
    cv2.imshow("\"Face Tracker\"", resizedImage)  

    # Izhod iz while loopa 
    if cv2.waitKey(1) == ord('q'):
        break

# Po zaklučku je treba vse sprostiti in zapreti
cap.release()
cv2.destroyAllWindows()
