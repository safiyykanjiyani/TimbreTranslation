#!python

import os
import sys

sys.path
sys.executable
import timbral_models
from csv import writer

list = []
filename = "oboe.wav"
timbre = timbral_models.timbral_extractor(filename)
list.append(filename)
list.append(timbre['hardness'])
list.append(timbre['depth'])
list.append(timbre['brightness'])
list.append(timbre['roughness'])
list.append(timbre['warmth'])
list.append(timbre['sharpness'])
list.append(timbre['boominess'])
list.append(timbre['reverb'])

with open('train.csv', 'a+', newline='') as write_obj:
    csv_writer = writer(write_obj)
    csv_writer.writerow(list)

print(timbre)
