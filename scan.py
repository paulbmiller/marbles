"""
Script to get the names of players of an end screen image of the podium of the
Marbles on Stream game. Current output :

Image 1 (End_w_podium.png) :
kamipandas
laliguedesombres
Faya_Siggy
vixndrv_3108 => vlxndrv_3108
dazaikogami
MEUsSn1 => MEUSSn1
hariboaxel
Jebogoss
LieTEESiCony => thomasinch
marginataur
Yerly
thepunishot
SOTA => Bouly_Ttv
hazemystery
mathiascsikos
floppi915
SteLeereli => Sakasapin
thekeyzak
SilentFartCH

Image 2 (End_w_podium2.png) :
LieTEESiCony => thomasinch
marginataur
aT => Yerly
thepunishot
SOTA => Bouly_Ttv
hazemystery
mathiascsikos
floppi915
SteLeereli => Sakasapin
thekeyzak
SilentFartCH
Heworlan
Crome => Gnou_
jean71260
4smeron
pavelnol => pavelno1
leolesourd
kaldra__
OTUTMETeecy => QuiKlaque
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image

def disp(img):
    plt.imshow(img, cmap='gray')

def dilate(img, n):
    return cv2.dilate(img, np.ones((n, n), np.uint8), iterations=1)

def erode(img, n):
    return cv2.erode(img, np.ones((n, n), np.uint8), iterations=1)

def takeSecond(elem):
    return (elem[0][1], elem[0][0])


"""
Getting names dynamically (not useful since pytesseract does this
automatically) and we can do this more easily by measuring the height of the
line (i.e. 41 pixels).

edges = cv2.bitwise_xor(dilate(img, 9), dilate(img, 7))
dil9 = dilate(img, 9)
contours, hierarchy = cv2.findContours(dil9, cv2.RETR_CCOMP,
                                       cv2.CHAIN_APPROX_SIMPLE)

words = []
for i in range(len(contours)):
    if hierarchy[0][i][3] == -1:
        topL_x, topL_y = np.amin(contours[i], axis=0)[0]
        botR_x, botR_y = np.amax(contours[i], axis=0)[0]
        words.append([(topL_x, topL_y), (botR_x, botR_y)])    

words.sort(key=takeSecond)


for word in words:
    if word[1][1] - word[0][1] >= 25:
        words.remove(word)
    else:
        img = cv2.rectangle(img, word[0], word[1], 255, 2)
"""


"""
To try different versions of page segmentation for pytesseract

for psm in range(0, 14):
    try:
        conf = '--psm {} --oem 3'.format(psm)
        names_string = pytesseract.image_to_string(names_img, config=conf)
        print('PSM : {}'.format(psm))
        print(names_string.replace('\x0c', ''))
    except FileNotFoundError:
        pass
"""

LINE_HEIGHT = 41

pytesseract.pytesseract.tesseract_cmd = \
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'

non_subs_color = (255, 255, 255)
subs_color = (247, 207, 171)
ogs_color = (210, 30, 249)
streamer_color = (136, 134, 248)

img_color = cv2.imread('End_w_podium.png')
names_x0, names_x1, names_y0, names_y1 = 656, 1011, 187, 966
names_color = img_color[names_y0:names_y1, names_x0:names_x1]
non_subs = cv2.inRange(names_color, (254, 255, 255), non_subs_color)

# non_subs = erode(dilate(non_subs, 3), 3)

subs = cv2.inRange(names_color, subs_color, subs_color)
ogs = cv2.inRange(names_color, ogs_color, ogs_color)
streamer = cv2.inRange(names_color, streamer_color, streamer_color)

img = cv2.bitwise_or(non_subs, subs)
img = cv2.bitwise_or(img, ogs)
img = cv2.bitwise_or(img, streamer)

"""
im = Image.fromarray(img)
im.save('End_w_podium_bw.png')
"""

char_wl = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

conf = '--psm 6 --oem 3 -c tessedit_char_whitelist={}'.format(char_wl)
names_string = pytesseract.image_to_string(img, config=conf)
print(names_string.replace('\x0c', ''))


"""
Trying names 1 by 1 in tesseract (worse results)

for i in range(18):
    temp = img[names_y0+i*LINE_HEIGHT:names_y0+(i+1)*LINE_HEIGHT,
               names_x0:names_x1]
    print(pytesseract.image_to_string(temp, config=conf).replace('\x0c', ''))
"""


img_color = cv2.imread('End_w_podium2.png')
names_x0, names_x1, names_y0, names_y1 = 654, 1006, 193, 972
names_color = img_color[names_y0:names_y1, names_x0:names_x1]
non_subs = cv2.inRange(names_color, non_subs_color, non_subs_color)
subs = cv2.inRange(names_color, subs_color, subs_color)
ogs = cv2.inRange(names_color, ogs_color, ogs_color)
streamer = cv2.inRange(names_color, streamer_color, streamer_color)

img = cv2.bitwise_or(non_subs, subs)
img = cv2.bitwise_or(img, ogs)
img = cv2.bitwise_or(img, streamer)

"""
im = Image.fromarray(img)
im.save('End_w_podium2_bw.png')
"""

names_string = pytesseract.image_to_string(img, config=conf)
print(names_string.replace('\x0c', ''))

