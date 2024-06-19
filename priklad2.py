user_button = Pin(0, Pin.IN)

count = 0
def handlerFalling(a):
    global count
    count = count + 1

user_button.irq(trigger=Pin.IRQ_FALLING, handler=handlerFalling)


while True:
    if(count == 0):
        setRGB(0,0,0)
        while(count == 0):
            pass
    elif (count == 1):
        setRGB(255,0,0)
        while(count == 1):
            setRGB(255,0,0)
            sleep_ms(50)
            setRGB(0,255,0)
            sleep_ms(50)
            setRGB(0,0,255)
            sleep_ms(50)
    elif (count == 2):
        while(count == 2):
            for i in range(12):
                np.fill((0,0,0))
                np[i] = (0,255,0)
                np.write()
                if (count != 2):
                    np.fill((0,0,0))
                    np.write()
                    break
                sleep(0.02)
        count = 0
        