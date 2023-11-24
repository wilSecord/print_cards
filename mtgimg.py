import scrython
import time
import requests
import cv2
import numpy as np

def make_image(cn, full):
    time.sleep(0.1)
    card = scrython.cards.Named(fuzzy=cn)
    file = cn + '.jpg'
    req = requests.get(card.image_uris(0, 'normal'))

    with open(file, 'wb') as f:
        f.write(req.content)

    img = cv2.imread(file)
    img = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    t1, t2 = 10, 360
    can = cv2.Canny(image=img, threshold1=t1, threshold2=t2)
    kernel1 = np.ones((2, 2), np.uint8)
    kernel2 = np.ones((2, 1), np.uint8)
    can = cv2.dilate(can, kernel1, iterations=1)
    can = cv2.erode(can, kernel2, iterations=1)
    if full:
        can = cv2.resize(can, (365, 512))
    else:
        can = cv2.resize(can, (300, 512))
    can = cv2.rotate(can, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    cv2.imwrite(file, cv2.bitwise_not(can))
