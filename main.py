"""A light loops around the NeoPixel strip, leaving a trail behind it

This code shows how to work with colors in HSV (hue-saturation-value) 
format and convert to RGB for display.
"""

import board
import analogio
import neopixel
import time
import math
from random import randint
from colorutils import hsv2rgb
 
pixpin = board.D0
numpix = 180
# brightness goes from 0 (no light) to 1.0 (full brightness)
# auto_write=True makes it so you don't have to call strip.write()
#   to change a value, but it makes things slower(?) 
strip = neopixel.NeoPixel(pixpin, numpix, brightness=1.0, auto_write=False)

pot = analogio.AnalogIn(board.A0)

hues=[234,200,156]

min_color_length=10
max_color_length=25

led_colors=[]
for i in range(numpix):
    led_colors.append([0,0,0])

def shuffle(list):
    swap=randint(1,2)
    tmp=list[swap]
    list[swap]=list[0]
    list[0]=tmp
    
def new_strip_hues(led_colors):
    global hues
    idx=0
    shuffle(hues)
    hue_idx=0
    while idx < numpix:
        hue=hues[hue_idx]
        hue_idx+=1
        if hue_idx >= len(hues):
            hue_idx=0
        length=randint(min_color_length,max_color_length)
        rgb=hsv2rgb((hue,255,255))
        for i in range(length):
            if idx >= numpix:
                break
            led_colors[idx][0]=rgb[0]
            led_colors[idx][1]=rgb[1]
            led_colors[idx][2]=rgb[2]
            idx+=1

new_strip_hues(led_colors)
for i in range(numpix):
    strip[i]=led_colors[i]
strip.write()

new_strip_hues(led_colors)
    
led_num=0

segment_len=numpix/2

while True:
    while led_num < segment_len and strip[led_num]==tuple(led_colors[led_num]):
        led_num+=1

    if led_num<segment_len:
        strip[led_num]=led_colors[led_num]
        strip[numpix-1-led_num]=led_colors[led_num]
        strip.write()
        led_num+=1

    if led_num >= segment_len:
        new_strip_hues(led_colors)
        led_num=0

    time.sleep(0.08)
