import sys
import re
import scrython
from escpos import printer
from escpos.constants import GS, ESC
import six
import time
from mtgimg import make_image
import xml.etree.ElementTree as et
import os

opt = sys.argv[1]

clean = False
cardb = False
deck = False
full = False

basics = ["Island", "Plains", "Mountain", "Swamp", "Forest", "Wastes"]
e = printer.Usb(0x04b8, 0x0202)

b = []
mb = []
sb = []
if len(sys.argv) > 4:
    full = sys.argv[4].upper() == "TRUE"

match opt:
    case "d":
        deck_loc = sys.argv[2]
        sb_bool = sys.argv[3]
        with open(deck_loc) as f:
            root = et.parse(f).getroot()
            for item in root:
                if item.keys():
                    name = item.attrib["Name"]
                    amnt = int(item.attrib["Quantity"])
                    if item.attrib["Sideboard"] == "false":
                        for i in range(amnt):
                            if name not in basics:
                                mb.append(scrython.cards.Named(fuzzy=name))
                            else:
                                if (amnt, name) not in b:
                                    b.append((amnt, name))
                    elif sb_bool == "y":
                        sb.append(scrython.cards.Named(fuzzy=name))
        
        for item in mb:
            time.sleep(0.1)
            make_image(item.name(), full)
            e.image("buf.jpg")
            if not full:
                e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        
        for item in b:
            time.sleep(0.1)
            e.text(str(item[0]) + ' ' + item[1] + '\n')
        if len(b):
            e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')

        for item in sb:
            time.sleep(0.1)
            make_image(item.name(), full)
            e.image("buf.jpg")
            if not full:
                e._raw(GS + b'V' + six.int2byte(66) + b'\x00')

    case "c":
        card = sys.argv[2]
        count = int(sys.argv[3])
        time.sleep(0.1)
        for i in range(count):
            make_image(card, full)
            e.image("buf.jpg")
            e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
    case "r":
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
