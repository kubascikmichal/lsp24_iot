import dht
from machine import Pin
from machine import ADC
from time import sleep

from u_thing_speak import ThingSpeak
from wifi import WiFi

dht_sensor = dht.DHT11(Pin(13))

fotoresistor = ADC(Pin(34))
fotoresistor.width(ADC.WIDTH_12BIT)
fotoresistor.atten(ADC.ATTN_11DB)

one_percent = (4095/100)

wifi_object = WiFi()
wifi_object.set_name_of_wifi_network("xxx")
wifi_object.set_password_of_wifi_network("xxx")
wifi_object.connect_to_existing_wifi_network()
    
THINGSPEAK_WRITE_API_KEY = 'xxx'
THINGSPEAK_READ_API_KEY = 'xxx'
CHANNEL_ID = 'xxx'

thing_speak = ThingSpeak()
thing_speak.set_write_api_key(THINGSPEAK_WRITE_API_KEY)
thing_speak.set_read_api_key(THINGSPEAK_READ_API_KEY)
thing_speak.set_channel_id(CHANNEL_ID)

pom = thing_speak.gather_data(0)
i = 1
if pom[0] == 0:
    print('general data:')
    for keys, values in pom[1].items():
        print(str(keys) + ': ' + str(values))    
    print()
    
    try:
        i = int(pom[1]['last_entry_id']) + 1
    except KeyError:
        i = 1

while True:
    foto_value = fotoresistor.read()
    foto_percentage = foto_value/one_percent
    
    dht_sensor.measure()
    dht_temperature = dht_sensor.temperature()
    dht_humidity = dht_sensor.humidity()

    print(str(i) + '.')
    print('DHT11 - temperature: ' + str(dht_temperature))
    print('DHT11 - humidity: ' + str(dht_humidity))
    print('fotoresistor - percentage: ' + str(foto_percentage))
    print()
    i = i + 1
    
    # sending data to ThingSpeak
    data = {'field1':dht_temperature, 'field2':dht_humidity, 'field3':foto_percentage}
    pom = thing_speak.send_data(data)


    sleep(60)
