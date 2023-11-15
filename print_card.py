import sys
import re
import scrython
from escpos import printer
from escpos.constants import GS, ESC
import six
import time
from mtgimg import make_image

opt = sys.argv[1]
if opt == "d":
    deck_loc = sys.argv[2]
    deck = True
    cardb = False
else:
    deck = False
if opt == "c":
    card = sys.argv[2]
    count = int(sys.argv[3])
    cardb = True
else:
    cardb = False

basics = ["Island", "Plains", "Mountain", "Swamp", "Forest", "Wastes"]
e = printer.Usb(0x04b8, 0x0202)

b = []
mb = []
sb = []
if deck:
    with open(deck_loc) as f:
        lines = f.readlines()[4:-1]
    
    for item in lines:
        amnt = int(re.findall(r'y="\d+"', item[:-14])[0][3])
        sideboard = False if re.findall(r'Sideboard="\w+"', item[:-14])[0][11:-1] == "false" else True
        name = re.findall(r'Name=".*"', item[:-14])[0][6:-1]
        if name not in basics:
            if sideboard:
                for i in range(amnt):
                    sb.append(scrython.cards.Named(fuzzy=name))
            else:
                for i in range(amnt):
                    sb.append(scrython.cards.Named(fuzzy=name))
        else:
            b.append((amnt, name))
    
    for item in mb:
        time.sleep(0.1)
        make_image(item.name())
        e.image("buf.jpg")
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
    
    for item in b:
        time.sleep(0.1)
        e.text(str(item[0]) + ' ' + item[1] + '\n')
    if len(b):
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
    
    e._raw(GS + b'V' + six.int2byte(66) + b'\x00')

    for item in sb:
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        time.sleep(0.1)
        make_image(item.name())
        e.image("buf.jpg")
if cardb:
    time.sleep(0.1)
    for i in range(count):
        make_image(card)
        e.image("buf.jpg")
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
