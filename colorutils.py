"""Utilities to help make working with colors easier

For now this just contains the hsv2rgb function, so it's probably best to do:

from colorutils import hsv2rgb

"""

def hsv2rgb(hsv):
    """Converts an (h,s,v) representation of a color into an (r,g,b) one
    Args:
         hsv: an (h,s,v) list with values from 0-255
    Returns:
         an (r,g,b) list with values from 0-255
    """
    (h,s,v)=hsv

    if s==0:
        # no saturation, so we can just do grayscale
        return (v,v,v)

    region=int(h/43)
    fpart=int((h-(region*43))*6)

    p = (v * (255 - s)) >> 8
    q = (v * (255 - ((s * fpart) >> 8))) >> 8
    t = (v * (255 - ((s * (255 - fpart)) >> 8))) >> 8

    if region==0:
        rgb=(v,t,p)
    elif region==1:
        rgb=(q,v,p)
    elif region==2:
        rgb=(p,v,t)
    elif region==3:
        rgb=(p,q,v)
    elif region==4:
        rgb=(t,p,v)
    else:
        rgb=(v,p,q)

    return rgb
    
