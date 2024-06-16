import sys, os, re, scrython, six, time
from escpos import printer
from escpos.constants import GS, ESC
from mtgimg import make_image, collect, get_rand
import xml.etree.ElementTree as et

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

if len(sys.argv) >= 4:
    full = sys.argv[4].upper() == "TRUE"
match opt:
    case "d":
        deck_loc = sys.argv[2]
        sb_bool = sys.argv[3]
        f = open(deck_loc)
        root = et.parse(f).getroot()
        for item in root:
            if item.keys() and item.attrib["Sideboard"] == "false":
                name = item.attrib["Name"]
                amnt = int(item.attrib["Quantity"])
                for i in range(amnt):
                    if name not in basics:
                        mb.append((amnt, name))
                    elif (amnt, name) not in b:
                        b.append((amnt, name))
            elif item.keys() and sb_bool == "y":
                sb.append((amnt, name))
        f.close()
        for item in mb:
            collect(item[1], "cards/mb/")

        for item in sb:
            collect(item[1], "cards/sb/")

        for item in mb:
            amnt = item[0]
            cn = item[1] + '.jpg'
            make_image("cards/mb/" + cn, full)
            for i in range(amnt):
                e.image("cards/mb/" + cn)
                if not full:
                    e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
            os.remove("cards/mb/" + cn)
        
        for item in b:
            e.text(str(item[0]) + ' ' + item[1] + '\n')
        if len(b):
            e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        
        for item in sb:
            amnt = item[0]
            cn = item[1] + '.jpg'
            make_image("cards/sb/" + cn, full)
            for i in range(amnt):
                e.image("cards/sb/" + cn)
            os.remove("cards/sb/" + cn)
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')

    case "c":
        card = sys.argv[2]
        fn = card + ".jpg"
        count = int(sys.argv[3])
        collect(card, "")
        make_image(fn, full)
        for i in range(count):
            e.image(fn, full)
            if full == False:
                e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        os.remove(fn)
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')

    case "m":
        cmc = sys.argv[2]
        cn = get_rand(cmc)
        print(cn)
        fn = cn + ".jpg"
        collect(cn, "")
        make_image(fn, True)
        e.image(fn, True)
        os.remove(fn)
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
        
    case "r":
        e._raw(GS + b'V' + six.int2byte(66) + b'\x00')
