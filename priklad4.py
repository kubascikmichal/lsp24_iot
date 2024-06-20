from machine import SoftI2C, Timer
import ssd1306
from dht import DHT22
my_dht = DHT22(Pin(37))
my_dht.measure()

photo = ADC(Pin(8, Pin.IN))
photo.width(ADC.WIDTH_13BIT)
photo.atten(ADC.ATTN_11DB)

def getPercentage():
    global photo
    minimum = 25000
    maximum = 65535
    interval = maximum - minimum
    return 100*(photo.read_u16() - minimum) / interval

counter = 0
def timerCallback(a):
    global counter
    counter = 1
    
clockCounter = 0
def clockCallback(a):
    global clockCounter, np
    np.fill((0,0,0))
    np[clockCounter % 12] = (0,255,0)
    np.write()
    clockCounter = clockCounter + 1
    

i2c = SoftI2C(scl=Pin(13), sda=Pin(14))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
name = "Michal"
surname = "Kubascik"

timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=timerCallback)

timer2 = Timer(1)
timer2.init(period=1000, mode=Timer.PERIODIC, callback=clockCallback)

oled.fill(0)
oled.text("Svetlo {:.2f} %".format(getPercentage()), 0,0)
oled.text(f"Teplota {my_dht.temperature()} C", 0,10)
oled.text(f"Vlhkost {my_dht.humidity()} %", 0,20)
oled.show()

while True:
    if counter == 1:
        counter = 0
        my_dht.measure()
        oled.fill(0)
        oled.text("Svetlo {:.2f} %".format(getPercentage()), 0,0)
        oled.text(f"Teplota {my_dht.temperature()} C", 0,10)
        oled.text(f"Vlhkost {my_dht.humidity()} %", 0,20)
        oled.show()
    else:
        pass
