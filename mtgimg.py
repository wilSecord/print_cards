import scrython
import random
import time
import json
import requests
import cv2
from PIL import Image
import numpy as np
import os

def make_image(fn, full):
    can = cv2.imread(fn)
    can = cv2.cvtColor(can, cv2.COLOR_BGR2GRAY)
    # img = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    # t1, t2 = 10, 360
    # can = cv2.Canny(image=img, threshold1=t1, threshold2=t2)
    # kernel1 = np.ones((2, 2), np.uint8)
    # kernel2 = np.ones((2, 1), np.uint8)
    # can = cv2.dilate(can, kernel1, iterations=1)
    # can = cv2.erode(can, kernel2, iterations=1)
    # if full:
    #     can = cv2.resize(can, (365, 512))
    # else:
    #     can = cv2.resize(can, (300, 512))
    # can = cv2.rotate(can, cv2.ROTATE_90_COUNTERCLOCKWISE)
    ### TEST ###
    # can = cv2.copyMakeBorder(can, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
    if full:
        can = cv2.resize(can, (365, 512))
    else:
        can = cv2.resize(can, (300, 512))
    cv2.imwrite("res.jpg", can)
    can = cv2.rotate(can, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite("rotate-res.jpg", can)
    rows, cols = np.shape(can)
    out = cv2.normalize(can, None, 0.0, 1.0, cv2.NORM_MINMAX)
    # img_p = Image.fromarray(can)
    # img_p = img_p.convert("L", dither=Image.Dither.FLOYDSTEINBERG)
    # for i in range(2, rows - 2):
    #     for j in range(2, cols - 2):
    #         # threshold step
    #         if (out[i][j] > 0.5):
    #             err = out[i][j] - 1
    #             out[i][j] = 1
    #         else:
    #             err = out[i][j]
    #             out[i][j] = 0

    #         # error diffusion step
    #         out[i][j + 1] = out[i][j + 1] + ((7 / 48) * err)
    #         out[i][j + 2] = out[i][j + 2] + ((5 / 48) * err)

    #         out[i + 1][j - 2] = out[i + 1][j - 2] + ((3 / 48) * err)
    #         out[i + 1][j - 1] = out[i + 1][j - 1] + ((5 / 48) * err)
    #         out[i + 1][j] = out[i + 1][j] + ((7 / 48) * err)
    #         out[i + 1][j + 1] = out[i + 1][j + 1] + ((5 / 48) * err)
    #         out[i + 1][j + 2] = out[i + 1][j + 2] + ((3 / 48) * err)

    #         out[i + 2][j - 2] = out[i + 2][j - 2] + ((1 / 48) * err)
    #         out[i + 2][j - 1] = out[i + 2][j - 1] + ((3 / 48) * err)
    #         out[i + 2][j] = out[i + 2][j] + ((5 / 48) * err)
    #         out[i + 2][j + 1] = out[i + 2][j + 1] + ((3 / 48) * err)
    #         out[i + 2][j + 2] = out[i + 2][j + 2] + ((1 / 48) * err)
    # out = cv2.normalize(out, None, 0.0, 255.0, cv2.NORM_MINMAX)
    # can = out[2:rows - 2, 2:cols -2]
    # img_p.save(fn)
    cv2.imwrite(fn, can)

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
    collect("Wear", "")
    make_image("Wear.jpg", True)

