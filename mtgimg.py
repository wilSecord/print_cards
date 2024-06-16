import scrython
import random
import time
import json
import requests
import cv2
import numpy as np
import os

def make_image(fn, full):
    img = cv2.imread(fn)
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
    
    cv2.imwrite(fn, cv2.bitwise_not(can))

def collect(cn, path):
    time.sleep(0.1)
    card = scrython.cards.Named(fuzzy=cn)
    file = cn + '.jpg'
    req = requests.get(card.image_uris(0, 'normal'))
    
    with open(path + file, 'wb') as f:
        f.write(req.content)

def gen_rand(cmc):
    page = 1
    try:
        card_search = scrython.cards.Search(q=f"cmc:{cmc} t:creature", page=page)
        cards = [item["name"] for item in card_search.data()]
    except scrython.ScryfallError as e:
        return []
    while card_search.has_more():
        page += 1
        time.sleep(0.1)
        try:
            card_search = scrython.cards.Search(q=f"cmc:{cmc} t:creature", page=page)
            cards += [item["name"] for item in card_search.data()]
        except scrython.ScryfallError as e:
            return []
    return cards

def get_rand(cmc):
    cards = json.load(open("momir.json", "r"))
    cn = random.choice(cards[str(cmc)])
    return cn

if __name__ == '__main__':
    print(get_rand(2))

