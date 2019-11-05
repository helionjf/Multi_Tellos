# Forked from https://github.com/TelloSDK/Multi-Tello-Formation
# This fork hosted at https://github.com/scubyd/Multi-Tello-Formation to support Python 3
# Updated and tested with Python 3.7

import socket


def set_ap(ssid, password):
    """
    A Function to set tello in AP mode
    :param ssid: the ssid of the network (e.g. name of the Wi-Fi)
    :param password: the password of the network
    :return:
    """

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
    my_socket.bind(('', 8889))
    cmd_str = 'command'
    print('Sending command %s' % cmd_str)
    my_socket.sendto(cmd_str.encode(), ('192.168.10.1', 8889))
    response, ip = my_socket.recvfrom(100)
    print('From %s received: %s' % (ip, response))

    cmd_str = 'ap %s %s' % (ssid, password)
    print('Sending command %s' % cmd_str)
    my_socket.sendto(cmd_str.encode(), ('192.168.10.1', 8889))
    response, ip = my_socket.recvfrom(100)
    print('From %s received: %s' % (ip, response))


# Example of setting Tello into command mode, and moving the Tello over to Access Point (AP) mode, i.e. make the
#  Tello connect directly to the specified WiFi network.  This setting will persist until the Tello is reset by
#  holding down the power button for ~5-10secs.
# Only works if server is connected directly to the Tello's own Wi-Fi.

set_ap('MY_WIFI_SSID', 'MY_WIFI_PASSWORD')
