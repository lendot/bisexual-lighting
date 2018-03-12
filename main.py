"""A light loops around the NeoPixel strip, leaving a trail behind it

This code shows how to work with colors in HSV (hue-saturation-value) 
format and convert to RGB for display.
"""

import board
import analogio
import neopixel
import time
import math
from random import randint,choice,random
from colorutils import hsv2rgb
 
pixpin = board.D0
numpix = 88
# brightness goes from 0 (no light) to 1.0 (full brightness)
# auto_write=True makes it so you don't have to call strip.write()
#   to change a value, but it makes things slower(?) 
strip = neopixel.NeoPixel(pixpin, numpix, brightness=1.0, auto_write=False)

pot = analogio.AnalogIn(board.A0)


# this just turns off all of the neopixels to start
# it is nice for making sure the code updated :)
strip.fill((0, 0, 0))

# calculate a logarithmic mapping for saturation values
saturation_mapping=[0]*256
saturation_mapping[0]=0
scale=255/math.log(5*255,2)
for i in range(1,256):
    saturation_mapping[i]=int(scale*math.log(i*5,2))

min_saturation=100
    
# saturation curve from one end to the other of a color segment
sine_curve=[0]*numpix
for i in range(numpix):
    x = i*(math.pi/numpix)
    y = int(155*math.sin(x))+100
#    if y<10:
#        y=10
    sine_curve[i]=y
#    sine_curve[i]=saturation_mapping[y]

# cosine curve for saturation sweep
cosine_curve=[0]*numpix
for i in range(numpix):
    x = i*(math.pi/numpix)
    y = int(155*math.cos(x))+100
    cosine_curve[i]=y



hues=(234,200,156)

min_color_length=4
max_color_length=8

led_colors=[]
for i in range(numpix):
    led_colors.append([0,0,0])

def new_strip_hues(led_colors):
    idx=0
    while idx < numpix:
        hue=choice(hues)
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

led_num=0
while True:
    strip[led_num]=(255,255,255)
    strip.write()

    time.sleep(0.02)
    
    strip[led_num]=led_colors[led_num]
    strip.write()

    led_num+=1
    if led_num >= numpix:
        new_strip_hues(led_colors)
        led_num=0

    time.sleep(0.05)
