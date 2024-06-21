"""
Class for work with WiFi.

Author: Bc. Tomas Baca
Project: Remote control for electrical buggy
"""

import network
import gc
import binascii
import time
import machine
import socket

class WiFi:
    """This class allows us to create or connect to WiFi network."""

    def __init__(self) -> None:
        """
        Constructor of the class.

        :param: None
        :return: None
        """
        self.__name_of_wifi_network = None
        self.__password_of_wifi_network = None
        self.__connection = None
        self.__final_list = None
        self.__wifi_state = 0
        self.__generating_header_and_footer = True
        self.__header = ''

    def set_name_of_wifi_network(self, name: str) -> int:
        """
        This function set name of the WiFi network.

        :param name: str
        :return: int

        Parameters:
        - first parameter is the name of the WiFi network that we
        are creating or to which we are connecting to.

        Return:
        - 0 - name was succesfully set.
        - 1 - first parameter can't be converted to string.
        """
        try:
            name = str(name)
        except ValueError:
            print("first parameter can't be converted to string")
            print('Class: WiFi, function: set_name_of_wifi_network')
            del name
            gc.collect()
            return 1
        self.__name_of_wifi_network = name
        del name
        gc.collect()
        return 0

    def set_password_of_wifi_network(self, password: str,
                                     supress_min_length: bool = False) -> int:
        """
        This function set password of the WiFi network.

        :param password: str
        :param supress_min_length: bool, default: False
        :return: int

        Parameters:
        - first parameter is the password of the WiFi network that we
        are creating or to which we are connecting to.Its minimal length
        is 8 characters. If the networks don't have password use as
        parameter empty string ("").
        - second parameter is used for suppressing minimal length of
        first parameter.
            - True: min lenght warning is suppressed
            - False: min length warning is not suppressed

        Return:
        - 0 - password was succesfully set.
        - 1 - first parameter can't be converted to string.
        - 2 - first parameter is too short.(minimal length 8 characters)
        """
        try:
            password = str(password)
        except ValueError:
            print("first parameter can't be converted to string")
            print('Class: WiFi, function: set_password_of_wifi_network')
            del password
            del supress_min_length
            gc.collect()
            return 1
        if len(password) != 0:
            if len(password) < 8 and supress_min_length is False:
                print("password must have at least 8 characters")
                print('Class: WiFi, function: set_password_of_wifi_network')
                del password
                del supress_min_length
                gc.collect()
                return 2

        self.__password_of_wifi_network = password
        del password
        del supress_min_length
        gc.collect()
        return 0

    def __find_existing_wifi_networks(self) -> None:
        """
        This function finds all wifi networks in range.

        :param: None
        :return: None
        """
        scanning_station = network.WLAN(network.STA_IF)
        scanning_station.active(True)

        network_list = scanning_station.scan()

        self.__final_list = []
        self.__final_list.append(['id', 'ssid', 'bssid', 'channel',
                                  'RSSI', 'security', 'hidden'])

        for i in range(0, len(network_list)):
            self.__final_list.append([str(i),
                                      str(network_list[i][0], 'UTF-8'),
                                      binascii.hexlify(network_list[i][1]),
                                      network_list[i][2],
                                      network_list[i][3],
                                      network_list[i][4],
                                      network_list[i][5]])
            del i
        scanning_station.active(False)

        del scanning_station
        del network_list
        gc.collect()

    def print_existing_networks(self) -> None:
        """
        This function prints existing networks in range.

        :param: None
        :return: None
        """
        self.__find_existing_wifi_networks()
        column_width = [None] * len(self.__final_list[0])

        for i in range(0, len(self.__final_list[0])):
            lengths = []
            for x in range(0, len(self.__final_list)):
                lengths.append(len(str(self.__final_list[x][i])))

            column_width[i] = max(lengths) + 4
            del lengths
            gc.collect()

        help_str = str("{: ^" + str(column_width[0]) + "} {: ^" +
                       str(column_width[1]) + "} {: ^" +
                       str(column_width[2]) + "} {: ^" +
                       str(column_width[3]) + "} {: ^" +
                       str(column_width[4]) + "} {: ^" +
                       str(column_width[5]) + "} {: ^" +
                       str(column_width[6]) + "}")

        for line in self.__final_list:
            print(help_str.format(*line))
        print()

        del column_width
        del help_str
        del i
        del line
        gc.collect()

    def print_existing_networks_without_password(self) -> None:
        """
        This function prints existing networks without password in range.

        :param: None
        :return: None
        """
        self.__find_existing_wifi_networks()
        column_width = [None] * len(self.__final_list[0])

        counter = 0
        for i in range(0, len(self.__final_list[0])):
            lengths = []
            for x in range(0, len(self.__final_list)):
                if (self.__final_list[x][5] == 0 or
                    self.__final_list[x][5] == 'security'):
                    lengths.append(len(str(self.__final_list[x][i])))
                    counter = counter + 1

            column_width[i] = max(lengths) + 4
            gc.collect()

        help_str = str("{: ^" + str(column_width[0]) + "} {: ^" +
                       str(column_width[1]) + "} {: ^" +
                       str(column_width[2]) + "} {: ^" +
                       str(column_width[3]) + "} {: ^" +
                       str(column_width[4]) + "} {: ^" +
                       str(column_width[5]) + "} {: ^" +
                       str(column_width[6]) + "}")
        counter = counter/6

        for line in self.__final_list:
            if line[5] == 0 or line[5] == "security":
                print(help_str.format(*line))
        print()

        del column_width
        del counter
        del help_str
        del i
        del line
        gc.collect()

    def __check_existence(self, name: str) -> int:
        """
        This function check whether there is wifi with name in range.

        :param name: str
        :return: int

        Parameters:
        - first parameter is name of the wifi that we want to check
        is in range.

        Return:
        - 0 - if wifi with given name exists.
        - 1 - first parameter can't be converted to string.
        - 2 - if wifi with given name does not exist.
        """
        try:
            name = str(name)
        except ValueError:
            print("first parameter can't be converted to string")
            print('Class: WiFi, function: __check_existence')
            del name
            gc.collect()
            return 1
        self.__find_existing_wifi_networks()
        for i in range(0, len(self.__final_list)):
            if self.__final_list[i][1] == name:
                del name
                gc.collect()
                return 0
        del i
        del name
        gc.collect()
        return 2

    def connect_to_existing_wifi_network(self, timeout: int = 15) -> int:
        """
        This function connect to existing wifi network if its in range.

        :param timeout: int, default = 15
        :return: int

        Parameters:
        - first parameter is timeout in second after which will device
        stop trying to connect to wifi network.

        Return:
        - 0 if I succesfully connected to network.
        - 1 if set timeout passed.
        - 2 if I dont set name of network by function:
        set_name_of_wifi_network
        - 3 if I dont set password for network by function:
        set_password_of_wifi_network
        - 4 if wifi network with choosen name does not exist
        - 5 if first parameter cant be converted to int
        - 6 if i used wrong password to the wifi network
        """
        if self.__name_of_wifi_network is None:
            print('At first you must set name of wifi network')
            print('Class: WiFi, function: connect_to_existing_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            del timeout
            gc.collect()
            return 2

        if self.__password_of_wifi_network is None:
            print("At first you must set password of wifi network")
            print('Class: WiFi, function: connect_to_existing_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            del timeout
            gc.collect()
            return 3

        if self.__check_existence(self.__name_of_wifi_network) == 2:
            print("WiFi network with choosen name does not exist")
            print('Class: WiFi, function: connect_to_existing_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            del timeout
            gc.collect()
            return 4

        try:
            timeout = int(timeout)
        except ValueError:
            print("first parameter cant be converted to int")
            print('Class: WiFi, function: connect_to_existing_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            del timeout
            gc.collect()
            return 5

        self.__connection = network.WLAN(network.STA_IF)
        self.__connection.active(True)
        self.__connection.connect(self.__name_of_wifi_network,
                                  self.__password_of_wifi_network)

        beginning = time.ticks_ms()
        timeout = timeout * 1000
        counter_pom = 0

        while self.__connection.isconnected() is False:
            end = time.ticks_ms()
            difference = time.ticks_diff(end, beginning)
            if difference > timeout:
                print()
                print("connection unseccesful - timeout pased")
                print("name of the wifi network: "
                      + self.__name_of_wifi_network)
                print("password of the wifi network: "
                      + self.__password_of_wifi_network)
                self.__wifi_state = 0
                self.__connection.active(False)
                self.__connection = None
                del beginning
                del timeout
                del end
                del difference
                gc.collect()
                return 1

            if int(self.__connection.status()) == 202:
                counter_pom = counter_pom + 1
                if counter_pom > 10:
                    print()
                    print("connection unseccesful - wrong password")
                    print("name of the wifi network: "
                          + self.__name_of_wifi_network)
                    print("password of the wifi network: "
                          + self.__password_of_wifi_network)
                    self.__wifi_state = 0
                    self.__connection.active(False)
                    self.__connection = None
                    del beginning
                    del timeout
                    del end
                    del difference
                    del counter_pom
                    gc.collect()
                    return 6                

        self.__wifi_state = 1
        print()
        print('##########################')
        print("connection succesfull")
        print("name of the wifi network: "
              + self.__name_of_wifi_network)
        print("password of the wifi network: "
              + self.__password_of_wifi_network)
        self.__print_current_if_config()
        del beginning
        del timeout
        del end
        del difference
        del counter_pom
        gc.collect()
        return 0

    def set_header(self, header: str) -> bool:
        """
        Function sets header that will be added to name of wifi network.

        :param header: str
        :return: bool

        Parameters:
        - First parameter is header that will be added to the beggining
        of wifi network name, in case that we are creating our own
        wifi network.

        Return:
        - True if header was succesfully set.
        - False if first parameter cant be converted to string.
        """
        try:
            header = str(header)
        except ValueError:
            print("first parameter can't be converted to string")
            print('Class: WiFi, function: set_header')
            del header
            gc.collect()
            return False
        self.__header = header
        del header
        gc.collect()
        return True

    def set_generating_header_and_footer(self, value: bool) -> bool:
        """
        Function set whether header and footer will be generated.

        :param value: bool
        :return: bool

        Parameters:
        - First parameter define whether we will be generating header
        and footer to the name of WiFi network when we are creating it.
            - True - header and footer will be generated.
            - False - header and footer wont be generated.

        Return:
        - True if setting was succesfully set.
        - False if first parameter cant be converted to bool.
        """
        try:
            value = bool(value)
        except ValueError:
            print("first parameter can't be converted to bool")
            print('Class: WiFi, function: set_generating_header_and_footer')
            del value
            gc.collect()
            return False
        self.__generating_header_and_footer = value
        del value
        gc.collect()
        return True

    def create_own_wifi_network(self) -> int:
        """
        This function creates own wifi network.

        :param: None
        :return: int

        Return:
        - 0 if I succesfully connected to network.
        - 1 if I dont set name of network by function:
        set_name_of_wifi_network
        - 2 if I dont set password for network by function:
        set_password_of_wifi_network
        - 3 if password for wifi network is shorter than 8 characters.
        """
        if self.__name_of_wifi_network is None:
            print('At first you must set name of wifi network')
            print('Class: WiFi, function: create_own_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            return 1

        if self.__password_of_wifi_network is None:
            print("At first you must set password of wifi network")
            print('Class: WiFi, function: create_own_wifi_network')
            self.__wifi_state = 0
            self.__connection = None
            return 2

        if len(self.__password_of_wifi_network) != 0:
            if len(self.__password_of_wifi_network) < 8:
                print("minimal password length is 8 characters")
                print('Class: WiFi, function: create_own_wifi_network')
                self.__wifi_state = 0
                self.__connection = None
                return 3

        if self.__generating_header_and_footer is True:
            beginning = self.__header
            middle = self.__name_of_wifi_network
            end = str(machine.unique_id())
            if len(beginning) != 0:
                self.__name_of_wifi_network = str(beginning + '_'
                                                  + middle + '_'
                                                  + end)
            else:
                self.__name_of_wifi_network = str(middle + '_' + end)
            del beginning
            del middle
            del end

        self.__connection = network.WLAN(network.AP_IF)
        self.__connection.active(True)

        if len(self.__password_of_wifi_network) != 0:
            self.__connection.config(essid=self.__name_of_wifi_network,
                                     password=self.__password_of_wifi_network,
                                     authmode=3)
        else:
            self.__connection.config(essid=self.__name_of_wifi_network,
                                     password='XXXXXXXX',
                                     authmode=0)

        while self.__connection.active() is False:
            pass

        self.__wifi_state = 2
        print()
        print('##########################')
        print("WiFi network created")
        print("name of the wifi network: "
              + self.__name_of_wifi_network)
        print("password of the wifi network: "
              + self.__password_of_wifi_network)
        self.__print_current_if_config()
        return 0

    def has_actual_wifi_access_to_internet(self) -> int:
        """
        This function test whether wifi has connection to internet.

        :param: None
        :return: int

        Return:
        - 0 if i have access to the internet.
        - 1 if i dont have access to the internet.
        - 2 if i am not curently connected to any network.
        """
        if self.__connection is None:
            print("I am not connected to any network")
            print('Class: WiFi, function: has_actual_wifi_access_to_internet')
            return 2

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        try:
            s.connect(socket.getaddrinfo('www.google.com', 80)[0][-1])
            s.close()
            print('This wifi network has access to the internet')
            del s
            gc.collect()
            return 0
        except OSError:
            s.close
            print('This wifi network dont have access to the internet')
            del s
            gc.collect()
            return 1

    def connect_to_wifi_network_with_access_to_internet(self) -> bool:
        """
        Function connects to open wifi network with access to internet.

        :param: None
        :return: bool

        Return:
        - True if I succesfully connected to open network with access
        to the internet.
        - False if I dont find any open network with access to the
        internet.
        """
        self.__find_existing_wifi_networks()
        for i in range(0, len(self.__final_list)):
            try:
                pom = self.__final_list[i]
                del pom
                gc.collect()
            except:
                continue
            
            if self.__final_list[i][5] == 0:
                self.set_name_of_wifi_network(str(self.__final_list[i][1]))
                self.set_password_of_wifi_network('')
                result = self.connect_to_existing_wifi_network()
                if result == 0:
                    result = self.has_actual_wifi_access_to_internet()
                    if result == 0:
                        del result
                        del i
                        gc.collect()
                        return True
                    else:
                        self.__connection.disconnect()
                        print('I am connecting to anothet network in range')
                del result
                gc.collect()
        del i
        gc.collect()
        return False

    def disconnect_from_wifi_network(self) -> None:
        """
        This function disconnect from currently connected WiFi network.

        :param: None
        :return: None
        """
        if self.__wifi_state == 1:
            self.__connection.disconnect()

    def end_work_with_wifi(self) -> None:
        """
        This function end work with current wifi.

        :param: None
        :return: None
        """
        if self.__wifi_state == 1:
            self.__connection.disconnect()
            self.__connection.active(False)
            self.__connection = None
            self.__wifi_state = 0
        elif self.__wifi_state == 2:
            self.__connection.active(False)
            self.__connection = None
            self.__wifi_state = 0

    def are_we_connected_to_access_point(self) -> int:
        """
        Function find if we (station) are connected to access point.

        :param: None
        :return: int

        Return:
        - 0 if station is connected to access point.
        - 1 if station is not connected to access point.
        - 2 if we are not operating as station.
        """
        if self.__wifi_state != 1:
            print('we are not operating as station')
            print('Class: WiFi, function: are_we_connected_to_access_point')
            return 2
        if self.__connection.isconnected() is True:
            return 0
        elif self.__connection.isconnected() is False:
            return 1

    def is_some_station_connected_to_as(self) -> int:
        """
        Function find if station is connected to as (access point).

        :param: None
        :return: int

        Return:
        - 0 if to access point is connected station.
        - 1 if to access point is not connected station.
        - 2 if we are not operating as access point.
        """
        if self.__wifi_state != 2:
            print('we are not operating as access point')
            print('Class: WiFi, function: is_some_station_connected_to_as')
            return 2
        if self.__connection.isconnected() is True:
            return 0
        elif self.__connection.isconnected() is False:
            return 1

    def __print_current_if_config(self) -> bool:
        """
        Function prints current if config.

        param: None
        return: bool

        Return:
        - True: if device is currenty operating as access point or
        station.
        - False: if device is currenty not operating as access point or
        station.
        """
        if self.__wifi_state == 0:
            return False
        else:
            helping_list = self.__connection.ifconfig()
            print('##########################')
            print("IP address of microcontroller: " + str(helping_list[0]))
            print("net mask is : " + str(helping_list[1]))
            print("IP address of gateway: " + str(helping_list[2]))
            print("IP address of DNS server: " + str(helping_list[3]))
            print('##########################')
            print()
            del helping_list
            gc.collect()
            return True

    def change_ip_configuration(self, ip_address: str = '',
                                network_mask: str = '',
                                default_gateway: str = '',
                                dns_server: str = '') -> int:
        """
        Function change IP address of device.

        :param ip_address: str default: ''
        :param network_mask: str default: ''
        :param default_gatewat: str default: ''
        :param dns_server: str default: ''
        :return: int

        Note: if some of the parameters is set to '', original
        value will be kept

        Parameters:
        - First parameter is new IP address of device.
        - Second parameter is new network mask of device.
        - Third parameter is default gateway of device.
        - Fourth parameter is dns server of device.

        Return:
        - 0 if new IP address was succesfully set.
        - 1 if first parameter cant be converted to str.
        - 2 if second parameter cant be converted to str.
        - 3 if third parameter cant be converted to str.
        - 4 if fourth parameter cant be converted to str.
        - 5 if we are not currently working as access point or station.
        """
        try:
            ip_address = str(ip_address)
        except ValueError:
            print('first parameter cant be converted to string')
            print('Class: WiFi, function: change_ip_configuration')
            del ip_address
            del network_mask
            del default_gateway
            del dns_server
            gc.collect()
            return 1

        try:
            network_mask = str(network_mask)
        except ValueError:
            print('second parameter cant be converted to string')
            print('Class: WiFi, function: change_ip_configuration')
            del ip_address
            del network_mask
            del default_gateway
            del dns_server
            gc.collect()
            return 2

        try:
            default_gateway = str(default_gateway)
        except ValueError:
            print('third parameter cant be converted to string')
            print('Class: WiFi, function: change_ip_configuration')
            del ip_address
            del network_mask
            del default_gateway
            del dns_server
            gc.collect()
            return 3

        try:
            dns_server = str(dns_server)
        except ValueError:
            print('third parameter cant be converted to string')
            print('Class: WiFi, function: change_ip_configuration')
            del ip_address
            del network_mask
            del default_gateway
            del dns_server
            gc.collect()
            return 4

        if self.__wifi_state == 0:
            print("we must first operate as access point or station")
            print('Class: WiFi, function: change_ip_configuration')
            del ip_address
            del network_mask
            del default_gateway
            del dns_server
            gc.collect()
            return 5

        if dns_server == '0.0.0.0':
            dns_server = ip_address

        current_values = self.__connection.ifconfig()
        current_values = list(current_values)

        if ip_address != '':
            current_values[0] = ip_address
        if network_mask != '':
            current_values[1] = network_mask
        if default_gateway != '':
            current_values[2] = default_gateway
        if dns_server != '':
            current_values[3] = dns_server

        current_values = tuple(current_values)
        self.__connection.ifconfig(current_values)

        self.__print_current_if_config()

        del ip_address
        del network_mask
        del default_gateway
        del dns_server
        gc.collect()
        return 0

# wifi_object = WiFi()

# wifi_object.print_existing_networks()

# print("############################################################")

# wifi_object.print_existing_networks_without_password()

# wifi_object.set_name_of_wifi_network("RB157")
# wifi_object.set_password_of_wifi_network("katka123548")
# wifi_object.connect_to_existing_wifi_network()
# print(wifi_object.are_we_connected_to_access_point())

# wifi_object.set_name_of_wifi_network('baca_test')
# wifi_object.set_password_of_wifi_network('veronika')
# wifi_object.set_header("KTK")
# wifi_object.set_generating_header_and_footer(True)
# wifi_object.create_own_wifi_network()
# wifi_object.change_ip_configuration('11.34.82.129','255.255.255.0',
#                                     '11.34.82.129','11.34.82.129')
# while wifi_object.is_some_station_connected_to_as() == 1:
#     pass
# print("station connected to us")

# wifi_object.disconnect_from_wifi_network()

# wifi_object.end_work_with_wifi()