import network
import sys
try:
    import usocket as socket
except:
    import socket
import network
import esp
import gc

from dht import DHT22

my_dht = DHT22(Pin(37))

ap = network.WLAN(network.AP_IF)

ssid_param = "zrfdťzifizugáuhzýihulih"
password_param = "123456789"

ap.config(ssid=ssid_param, authmode = 3, password=password_param)
ap.active(True)

while ap.active() == False:
    pass

print(ap.ifconfig())

def web_page(temp, hum):
    return """
        <html>
        <body>
        <p> Teplota {:.2f} vlhkost {:.2f} </p>
        </body>
        </html>
        """.format(temp, hum)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

    conn, addr = s.accept()
    request = conn.recv(1024)
    my_dht.measure()
    response = web_page(my_dht.temperature(), my_dht.humidity())
    conn.send(response)
    conn.close()

