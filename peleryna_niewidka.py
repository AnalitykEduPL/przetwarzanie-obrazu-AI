import cv2
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
# Argument wejściowy
parser.add_argument("--video", help = "Ścieżka do pliku który chcesz przetworzyć. Bez argumentu video będzie brane z kamerki urządzenia")

args = parser.parse_args()

print("""

Pelerynka niewidka jest ładowana

Przygotuj się na Magię technologii :)

    """)

# Tworzenie obiektu pracującego na pliku video
cap = cv2.VideoCapture(args.video if args.video else 0)
width = int(cap.get(3))
height = int(cap.get(4))

# Definicja atrybutów w tym kodeka który będzie użyty to zapisania pliku wyjściowego
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (width, height))

# Czas dla kamery, aby zdążyła się wczytać
time.sleep(3)
count = 0
background = 0

# Zapisujemy pierwsze 60 klatek jako obraz podstawowy. Przy ustawieniu 30 klates/sek będą to pierwsze 2 sekundy
for i in range(60):
    ret, background = cap.read()

# background = np.flip(background,axis=1)

while (cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        break
    count += 1
    # img = np.flip(img,axis=1)

    # Zamiana reprezentacji kolory z BGR na HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Tworzenie maski kolorów które będą reprezentować "pelerynke niewidkę"
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2

    # Działania przetwarzające maski niezbędne do stworzenia efektu pelerynki niewidki
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    mask2 = cv2.bitwise_not(mask1)

    # Tworzenie widoku wyjściowego przy użyciu maski
    res1 = cv2.bitwise_and(background, background, mask=mask1)
    res2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    print(type(final_output))

    out.write(final_output)

    cv2.imshow('Magia Technologi !!!', final_output)

    # wciśnij ESC aby zatrzymać przetwarzanie/nagrywanie
    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()