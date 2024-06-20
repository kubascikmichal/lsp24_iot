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
    minimum = 37000
    maximum = 65535
    interval = maximum - minimum
    val = 100*(photo.read_u16() - minimum) / interval
    if val < 0:
        return 0
    elif val > 100:
        return 100
    else:
        return val

counter = 0
def timerCallback(a):
    global counter
    counter = counter + 1
    
clockCounter = 0
def clockCallback(a):
    global clockCounter, np
    np.fill((0,0,0))
    np[clockCounter % 12] = (0,255,0)
    np.write()
    clockCounter = clockCounter + 1
    
def photoCallback(a):
    val = getPercentage()/100
    setRGB(0, int(1023*val), 0)

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

timer3 = Timer(2)
timer3.init(period=50, mode=Timer.PERIODIC, callback=photoCallback)

oled.fill(0)
oled.text("Svetlo {:.2f} %".format(getPercentage()), 0,0)
oled.text(f"Teplota {my_dht.temperature()} C", 0,10)
oled.text(f"Vlhkost {my_dht.humidity()} %", 0,20)
oled.show()
pom_counter = counter
while True:
    if counter != pom_counter:
        pom_counter = counter
        if (counter % 30) == 0:
            my_dht.measure()
        oled.fill(0)
        oled.text("Svetlo {:.2f} %".format(getPercentage()), 0,0)
        oled.text(f"Teplota {my_dht.temperature()} C", 0,10)
        oled.text(f"Vlhkost {my_dht.humidity()} %", 0,20)
        oled.show()
    else:
        pass
