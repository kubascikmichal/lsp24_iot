from neopixel import NeoPixel
from machine import Pin, PWM, ADC
from time import sleep, sleep_ms

np = NeoPixel(Pin(40),12)
np.fill((0,0,0))
np.write()

red = Pin(33, Pin.OUT)
green = Pin(18, Pin.OUT)
blue = Pin(16, Pin.OUT)

red_pwm = PWM(red,1000)
green_pwm = PWM(green,1000)
blue_pwm = PWM(blue,1000)

photo = ADC(Pin(8, Pin.IN))
photo.width(ADC.WIDTH_13BIT)
photo.atten(ADC.ATTN_11DB)

def setRGB(r,g,b):
    blue_pwm.duty(b)
    red_pwm.duty(r)
    green_pwm.duty(g)

setRGB(500,500,0)

np[6] = (255,0,0)
np.write()

while True:
    for i in range(12):
        np.fill((0,0,0))
        np[i] = (255,150,50)
        np.write()
        sleep(1)