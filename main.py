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

# pin the NeoPixel data line is attached to
pixpin = board.D0
# number of LEDs
numpix = 180

# pin the potentiometer is attached to
potpin = board.A0

# set up the neopixel strip
strip = neopixel.NeoPixel(pixpin, numpix, brightness=1.0, auto_write=False)

# set up the ADC for the potentiometer
pot = analogio.AnalogIn(potpin)

# these are the hues for the bisexual flag colors
hues=[234,200,156]

brightness = 255

# each of the current computed rgb values
rgb_colors=[]
# shuffled index into rgb_colors
random_rgb=[]
for i in range(len(hues)):
    rgb_colors.append([0,0,0])
    random_rgb.append(i)

# minimum/maximum number of contiguous LEDs with the same color
min_color_length=10
max_color_length=25

# we'll generate colors for half the length of the strip
# and mirror on the other half
segment_len=numpix/2

# these will hold the indexes into rgb_colors
led_colors=[]
# for updating brightness on leds we haven't changed yet
old_led_colors=[]
for i in range(segment_len):
    led_colors.append(0)
    old_led_colors.append(0)

# iteration speed range
min_sleep=0.03
max_sleep=0.2

# brightness range
min_brightness=64
max_brightness=255



# todo: make this work for lists of any length
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

# create a new random color sequence
def new_strip_colors(random_rgb,led_colors,old_led_colors):
    shuffle(random_rgb)
    # save the current color sequence
    for i in range(len(led_colors)):
        old_led_colors[i]=led_colors[i]
    idx=0
    color_idx=0
    while idx < len(led_colors):
        rgb_idx=random_rgb[color_idx]
        color_idx+=1
        if color_idx >= len(random_rgb):
            color_idx=0
        length=randint(min_color_length,max_color_length)
        for i in range(length):
            if idx >= len(led_colors):
                break
            led_colors[idx]=rgb_idx
            idx+=1

# map a range of input values to a range of output values
# Based off of Arduino map function
def map(val,in_min,in_max,out_min,out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# knock down the precision of the read value to alleviate jitter
last_pot_val=pot.value>>8
brightness=int(map(last_pot_val,0,255,min_brightness,max_brightness))
sleep_time=map(255-last_pot_val,0,255,min_sleep,max_sleep)
calculate_rgb(hues,rgb_colors,brightness)

# setup an initial sequence to write out before iterating
new_strip_colors(random_rgb,led_colors,old_led_colors)
for i in range(len(led_colors)):
    strip[i]=strip[numpix-1-i]=rgb_colors[led_colors[i]]
strip.write()

# create our first sequence to iterate over
new_strip_colors(random_rgb,led_colors,old_led_colors)
    
led_num=0

pot_check=5

while True:
    pot_check-=1
    if pot_check<=0:
        pot_check=5
        pot_val=pot.value>>8
#        pot_val=pot.value
        
        if pot_val!=last_pot_val:
            print(pot_val)
            brightness=int(map(pot_val,0,255,min_brightness,max_brightness))
            sleep_time=map(255-pot_val,0,255,min_sleep,max_sleep)
            calculate_rgb(hues,rgb_colors,brightness)
            for i in range(len(led_colors)):
                if i < led_num:
                    strip[i]=strip[numpix-1-i]=rgb_colors[led_colors[i]]
                else:
                    # we haven't gotten to these LEDs yet
                    strip[i]=strip[numpix-1-i]=rgb_colors[old_led_colors[i]]
                    
            strip.write()
            last_pot_val=pot_val
    
    while led_num < segment_len and strip[led_num]==tuple(rgb_colors[led_colors[led_num]]):
        led_num+=1

    if led_num<segment_len:
        strip[led_num]=strip[numpix-1-led_num]=rgb_colors[led_colors[led_num]]
        strip.write()
        led_num+=1

    if led_num >= segment_len:
        new_strip_colors(random_rgb,led_colors,old_led_colors)
        led_num=0

    time.sleep(sleep_time)
