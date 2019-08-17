import cv2
import glob

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

images = glob.glob("*.jpg")

for image in images:
    img = cv2.imread(image, 1)
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = cascade.detectMultiScale(gray_scale, scaleFactor=1.05, minNeighbors=5)
    for x, y, width, height in face:
        img = cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 3)
    resized = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
    cv2.imwrite("Deected Faces.jpg" + image, resized)
