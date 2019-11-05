***Tello Edu SDK 2.0 - for Python 3***

This is a fork from the official SDK, hosted at https://github.com/TelloSDK/Multi-Tello-Formation.  The priority changes were to make the Python library compatible with Python 3, and to enable more advanced control from within Python.  Specifically, that means transforming the simple text-driven commands into Python functions, which can then be extended.

The install scripts which formed part of the official SDK version contained a large binary copy of PIP, and so have been removed.  The very few dependencies can be easily installed by the user.

Key functionality will be described below as it is tested and updated, as an English language update from the original Chinese readme.

***Configuration / Setup***

Only two non-standard libraries are required - ```netifaces``` and ```netaddr```.  These can be installed on Mac or Linux with the following commands:
```
pip3 install netifaces
pip3 install netaddr
```
For Windows, I understand the following commands are needed:
```
python -m pip install netifaces
python -m pip install netaddr
```
***Test Flight - Single Tello***

A single Tello can be used in its default mode, with the controller (i.e. the device running this Python code) connected directly to the Tello's WiFi network.  This WiFi network will be named in the format ```TELLO-ABC123```, where ABC123 is the last 6 digits of the Tello's MAC address which can be found on a sticker inside the battery compartment.

Firstly, running ```python multi_tello_test.py ip.txt``` will connect to the Tello, and return its serial number and IP address.  This serial number is important for the next steps...

To get the Tello flying, you should edit the ```test_for_1.txt``` script in the ```example_script``` sub-folder.  It current contains the following:
```
scan 1
battery_check 20
correct_ip
1=0TQDF72EDB2BP8
*>takeoff
sync 15
1>go 50 0 80 100
sync 15
1>flip r
sync 15
*>land
```
Initially, you just need to change the line which says ```1=0TQDF72EDB2BP8```, substituting your serial number so it follows ```1=```.

Having made that change, run ```python multi_tello_test.py example_script/test_for_1.txt```.  You should see the Tello takeoff, fly forward, rotate 360 degrees, return to its starting point, and land.  At this point congratulations, you've got the Tello flying.

***Enabling Access to Multiple Tellos***

So far we've been connected directly to a single Tello's own WiFi network.  This is fine for a single Tello, but won't allow you to fly multiple Tellos at once - you can only (usually) connect to a single WiFi network at once.

Ryze have thought of this, and a significant upgrade to the Tello Edu is the ability to make the Tello connect to an existing WiFi network - in your home, office, or anywhere.

You can make as many Tellos as you like connect to the same WiFi network.  You only need to configure this once, and then the Tello will always connect to the same WiFi network whenever it is turned on.  If you want to change the WiFi network, or have any problems, you can reset the Tello by turning it on, and then holding down the power button for ~5-10secs; until the status lights go out.  This resets it and you'll be able to connect directly to the Tello's own WiFi network again.

To connect a Tello to a WiFi network, first edit the ```formation_setup.py``` file and put your own WiFi details into the last line of that file - it current says ```set_ap('MY_WIFI_SSID', 'MY_WIFI_PASSWORD')```.

Once your WiFi details are entered and saved, connect to one of your Tellos' own WiFi networks.  Then by running ```python formation_setup.py```, your Tello will be configured automatically.  It only takes a few seconds, after which it will restart and connect itself to your WiFi network.  Repeat this process for all of your Tellos.

Once done, when you connect back to your own WiFi network you will be able to to again run the single-Tello scripts above.  But it also opens up the possibility of connecting to multiple Tellos at once.

***Test Flight - Multiple Tellos***

To be completed...


