from neopixel import NeoPixel
from machine import Pin

np = NeoPixel(Pin(40),12)

np.fill((0,0,0))
np.write()