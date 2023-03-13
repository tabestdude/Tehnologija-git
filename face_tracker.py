import numpy
import cv2

# version 0.3

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    # [0] - x(vodoravno) // [1] - y(navpicno)
    print("tup2[0]:{}", levo_zgoraj[0])
    print("tup2[1]:{}", levo_zgoraj[1])
    print("tup2[0]:{}", desno_spodaj[0])
    print("tup2[1]:{}", desno_spodaj[1])
    spodnja_meja_koze = 0
    zgornja_meja_koze = 0
    return (spodnja_meja_koze, zgornja_meja_koze)

def zmanjsaj_sliko(slika):
    pass

def obdelaj_sliko(slika, okno_sirina, okno_visina, barva_koze_spodaj, barva_koze_zgoraj):
    pass

def prestej_piksle_z_barvo_koze(podslika, barva_koze_spodaj, barva_koze_zgoraj):
    pass


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

drawing = False # True if mouse is pressed
ix, iy = -1, -1 # Upper left
jx, jy = -1, -1 # Down right
doneDrawing = False # True after button up

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, doneDrawing, jx, jy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(img, (ix, iy), (x, iy), (0, 255, 0), 1)        
            cv2.line(img, (ix, iy), (ix, y), (0, 255, 0), 1)   
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        doneDrawing = True
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1, 8)
        jx, jy = x, y
        
cv2.namedWindow("PrvaSlika")
cv2.setMouseCallback("PrvaSlika", draw_rectangle)
# če imam samo en "cap.read()" je prva slika cela zelene 
# ugibam da zato ker uporabljam telefon za webcam in je nek problem z aplikacijo
# ki jo uporabljam za prenos videa na webcam feed (Iriun webcam)
firstRet, firstFrame = cap.read()
firstRet, firstFrame = cap.read()
firstRet, firstFrame = cap.read()
firstRet, firstFrame = cap.read()
img = firstFrame
while True:
    cv2.imshow('PrvaSlika', img)
    if cv2.waitKey(1) == ord('q'):
        break
    if not drawing:
        if doneDrawing:
            cv2.imshow('PrvaSlika', img)
            break

lower_upper_skin_color_limit = doloci_barvo_koze(img, (ix, iy), (jx, jy))
cv2.namedWindow("Kamera")
while True:
    # Capture frame-by-frame
        
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    imgDraw = numpy.zeros(frame.shape, numpy.uint8)
    imgDraw = cv2.circle(imgDraw,(200,200),30,(255,0,0),3)
    final = frame | imgDraw # cv22.add(s1,s2)
    
    # Display the resulting frame
    cv2.imshow('Kamera', final)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
