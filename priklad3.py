from dht import DHT22
from machine import Timer

my_dht = DHT22(Pin(37))

def showTemHum(a):
    global my_dht
    my_dht.measure()
    print(my_dht.temperature())
    print(my_dht.humidity())

timer = Timer(0)
timer.init(period=2000, mode=Timer.PERIODIC, callback=showTemHum)

while True:
    pass
