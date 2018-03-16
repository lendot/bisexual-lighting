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

brightness = 255

hues=[234,200,156]
rgb_colors=[]
for i in range(len(hues)):
    rgb_colors.append([0,0,0])

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

# calculate the rgb values for each hue at the current brightness
def calculate_rgb(hues,rgb_colors,brightness):
    for i in range(len(hues)):
        hue=hues[i]
        rgb=hsv2rgb((hue,255,brightness))
        rgb_colors[i][0]=rgb[0]
        rgb_colors[i][1]=rgb[1]
        rgb_colors[i][2]=rgb[2]
    
def new_strip_colors(rgb_colors,led_colors):
    global hues
    idx=0
    shuffle(rgb_colors)
    color_idx=0
    while idx < numpix:
        rgb=rgb_colors[color_idx]
        color_idx+=1
        if color_idx >= len(rgb_colors):
            color_idx=0
        length=randint(min_color_length,max_color_length)
        for i in range(length):
            if idx >= numpix:
                break
            led_colors[idx][0]=rgb[0]
            led_colors[idx][1]=rgb[1]
            led_colors[idx][2]=rgb[2]
            idx+=1

def map(val,in_min,in_max,out_min,out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


min_sleep=0.03
max_sleep=0.2

# knock down the precision of the read value to alleviate jitter
last_pot_val=pot.value>>12
brightness=int(map(last_pot_val,0,15,128,255))
sleep_time=map(15-last_pot_val,0,15,min_sleep,max_sleep)
calculate_rgb(hues,rgb_colors,brightness)

new_strip_colors(rgb_colors,led_colors)
for i in range(numpix):
    strip[i]=led_colors[i]
strip.write()

new_strip_colors(rgb_colors,led_colors)
    
led_num=0

segment_len=numpix/2


pot_check=5

while True:
    pot_check-=1
    if pot_check<=0:
        pot_check=5
        pot_val=pot.value>>12
#        pot_val=pot.value
        
        if pot_val!=last_pot_val:
            brightness=int(map(pot_val,0,15,128,255))
            sleep_time=map(15-pot_val,0,15,min_sleep,max_sleep)
            calculate_rgb(hues,rgb_colors,brightness)
            last_pot_val=pot_val
    
    while led_num < segment_len and strip[led_num]==tuple(led_colors[led_num]):
        led_num+=1

    if led_num<segment_len:
        strip[led_num]=led_colors[led_num]
        strip[numpix-1-led_num]=led_colors[led_num]
        strip.write()
        led_num+=1

    if led_num >= segment_len:
        new_strip_colors(rgb_colors,led_colors)
        led_num=0

    time.sleep(sleep_time)
