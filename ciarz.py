from machine import Pin
from machine import ADC
from machine import PWM
from hcsr04 import HCSR04
import time

cny70_left = ADC(Pin(35))
cny70_left.atten(ADC.ATTN_11DB)
cny70_left.width(ADC.WIDTH_12BIT)

cny70_middle = ADC(Pin(36))
cny70_middle.atten(ADC.ATTN_11DB)
cny70_middle.width(ADC.WIDTH_12BIT)

cny70_right = ADC(Pin(39))
cny70_right.atten(ADC.ATTN_11DB)
cny70_right.width(ADC.WIDTH_12BIT)

engine_enable = Pin(22, Pin.OUT, value = 1)

engine_left_forward = PWM(Pin(4), freq = 5000, duty = 0)
engine_left_reverse = PWM(Pin(0), freq = 5000, duty = 0)

engine_right_forward = PWM(Pin(2), freq = 5000, duty = 0)
engine_right_reverse = PWM(Pin(15), freq = 5000, duty = 0)

increased_speed = 500
normal_speed = 400
slowed_speed = 300
sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

while True:
    print(cny70_left.read())
    print(cny70_middle.read())
    print(cny70_right.read())
    distance = sensor.distance_cm()
    if(distance < 6 and distance > 1):
        engine_left_forward.duty(0)
        engine_right_forward.duty(0)
        distance = sensor.distance_cm()
    elif cny70_left.read() < 100:
        engine_left_forward.duty(slowed_speed)
        engine_right_forward.duty(increased_speed)
    elif cny70_middle.read() < 100:
        engine_left_forward.duty(normal_speed)
        engine_right_forward.duty(normal_speed)
    elif cny70_right.read() < 100:
        engine_left_forward.duty(increased_speed)
        engine_right_forward.duty(slowed_speed)
    
#     time.sleep(0.005)
#     time.sleep(2)
#     else:
#         engine_left_forward.duty(0)
#         engine_right_forward.duty(0)
