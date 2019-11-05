# Forked from https://github.com/TelloSDK/Multi-Tello-Formation
# Additional code for reading the state of the Tello is based on
#  https://github.com/dji-sdk/Tello-Python/blob/master/tello_state.py
# This fork hosted at https://github.com/scubyd/Multi-Tello-Formation to support Python 3
# Updated and tested with Python 3.7

import threading
import socket
import time
import netifaces
import netaddr
from netaddr import IPNetwork
from collections import defaultdict
from stats import Stats


class Tello:
    """
    A wrapper class to interact with Tello
    Communication with Tello is handled by Tello_Manager
    """
    def __init__(self, tello_ip, tello_manager):
        self.tello_ip = tello_ip
        self.tello_manager = tello_manager

    def send_command(self, command):
        return self.tello_manager.send_command(command, self.tello_ip)


class TelloManager:

    def __init__(self):

        # Socket for sending and receiving commands
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # Socket for receiving status messages from Tello - needs to be bound by enable_status() function
        self.status_port = 8890
        self.status_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status_thread = None
        self.status = {}

        # Thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip_list = []
        self.tello_list = []
        self.log = defaultdict(list)

        self.COMMAND_TIME_OUT = 9.0

        self.last_response_index = {}
        self.str_cmd_index = {}

    def find_available_tello(self, num, first_ip=1, last_ip=254):
        """
        Find available tello in server's subnets
        :param num: Number of Tello this method is expected to find
        :param first_ip: First IP address to search
        :param last_ip: Last IP address to search
        :return: None
        """
        print('[Start_Searching]Searching for %s available Tello...' % num)

        subnets, address = self.get_subnets()
        possible_addr = []

        for subnet, netmask in subnets:
            for ip in IPNetwork('%s/%s' % (subnet, netmask)):
                # only search addresses between (or equal to) the specified first and last IP addresses
                if not (first_ip <= int(str(ip).split('.')[3]) <= last_ip):
                    continue
                possible_addr.append(str(ip))

        while len(self.tello_ip_list) < num:
            print('[Still_Searching]Trying to find Tello in subnets...')

            # Delete any Tellos that have already been found from possible_addr list, while we keep searching for the
            #  remaining Tellos
            for tello_ip in self.tello_ip_list:
                if tello_ip in possible_addr:
                    possible_addr.remove(tello_ip)

            # Try connecting to each possible_addr, skipping the server's own IP
            for ip in possible_addr:
                if ip in address:
                    continue

                # Record this command in the log, and send it
                self.log[ip].append(Stats('command', len(self.log[ip])))
                self.socket.sendto('command'.encode(), (ip, 8889))

            # Wait a few seconds for a response before trying again - but regularly check to see if we've already found
            #  all Tellos, in which case we can break out early
            for _ in range(1, 8):
                time.sleep(0.5)
                if len(self.tello_ip_list) >= num:
                    break

        # Remove non-Tello addresses from the log, by recreating the log with only Tello-matching entries
        temp = defaultdict(list)
        for ip in self.tello_ip_list:
            temp[ip] = self.log[ip]
        self.log = temp

    @staticmethod
    def get_subnets():
        """
        Look through the server's internet connection and
        returns subnet addresses and server ip
        :return: list[str]: subnets
                 list[str]: addr_list
        """
        subnets = []
        ifaces = netifaces.interfaces()
        addr_list = []
        for this_iface in ifaces:
            addrs = netifaces.ifaddresses(this_iface)

            if socket.AF_INET not in addrs:
                continue

            # Get ipv4 stuff
            ip_info = addrs[socket.AF_INET][0]
            address = ip_info['addr']
            netmask = ip_info['netmask']

            # Limit range of search. This will work for router subnets
            if netmask != '255.255.255.0':
                continue

            # Create ip object and get the network details
            # Note CIDR is a networking term, describing the IP/subnet address format
            cidr = netaddr.IPNetwork('%s/%s' % (address, netmask))
            network = cidr.network
            subnets.append((network, netmask))
            addr_list.append(address)
        return subnets, addr_list

    def get_tello_list(self):
        return self.tello_list

    def enable_status(self, interval, print_all):
        self.status_socket.bind((self.local_ip, self.status_port))

        # thread for receiving status
        self.status_thread = threading.Thread(target=self._receive_status_thread, args=(interval, print_all))
        self.status_thread.daemon = True
        self.status_thread.start()

    def send_command(self, command, ip):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either because of timeout or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """

        # NOTE: Unclear what the multi_cmd flags are for...
        command_sof_1 = ord(command[0])
        command_sof_2 = ord(command[1])
        if command_sof_1 == 0x52 and command_sof_2 == 0x65:
            multi_cmd_send_flag = True
        else:
            multi_cmd_send_flag = False

        if multi_cmd_send_flag:
            self.str_cmd_index[ip] = self.str_cmd_index[ip] + 1
            for num in range(1, 5):
                str_cmd_index_h = self.str_cmd_index[ip] / 128 + 1
                str_cmd_index_l = self.str_cmd_index[ip] % 128
                if str_cmd_index_l == 0:
                    str_cmd_index_l = str_cmd_index_l + 2
                cmd_sof = [0x52, 0x65, str_cmd_index_h, str_cmd_index_l, 0x01, num + 1, 0x20]
                cmd_sof_str = str(bytearray(cmd_sof))
                cmd = cmd_sof_str + command[3:]
                self.socket.sendto(cmd.encode(), (ip, 8889))

            print('[Multi_Command]----IP:%s----Command:%s' % (ip, command[3:]))
            real_command = command[3:]
        else:
            self.socket.sendto(command.encode(), (ip, 8889))
            print('[Single_Command]----IP:%s----Command:%s' % (ip, command))
            real_command = command
        
        self.log[ip].append(Stats(real_command, len(self.log[ip])))
        start = time.time()
        while not self.log[ip][-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.COMMAND_TIME_OUT:
                print('[Not_Get_Response]Max timeout exceeded for command: %s' % real_command)
                return

    def _receive_thread(self):
        """ Listen to responses from the Tello.

        Runs continuously in its own thread, setting self.response to whatever the Tello last returned

        """

        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                self.response = self.response.decode()
                ip = ''.join(str(ip[0]))

                # Capture any new Tellos if they appear during runtime
                if self.response.upper() == 'OK' and ip not in self.tello_ip_list:
                    print('[Found_Tello]----New Tello ip is:%s' % ip)
                    self.tello_ip_list.append(ip)
                    self.last_response_index[ip] = 0
                    self.tello_list.append(Tello(ip, self))
                    self.str_cmd_index[ip] = 1

                # NOTE: Unclear what Multi_Response represents...
                response_sof_part1 = ord(self.response[0])
                response_sof_part2 = ord(self.response[1])
                if response_sof_part1 == 0x52 and response_sof_part2 == 0x65:
                    response_index = ord(self.response[5])
                    if response_index < self.last_response_index[ip]:
                        print('[Multi_Response]----IP:%s----Response:   %s ----' % (ip, self.response[7:]))
                        self.log[ip][-1].add_response(self.response[7:], ip)
                    self.last_response_index[ip] = response_index
                else:
                    print('[Single_Response]----IP:%s----Response:%s ----' % (ip, self.response))
                    self.log[ip][-1].add_response(self.response, ip)
                         
            except socket.error as exc:
                print('[Exception_Error]Caught exception socket.error : %s' % exc)

    def _receive_status_thread(self, interval, print_all):
        """ Listen to status messages from the Tello.

            Runs continuously in its own thread, setting self.status[ip] for each Tello
        """

        while True:
            try:
                response, ip = self.status_socket.recvfrom(1024)
                response = response.decode()
                if response == 'ok':
                    continue
                ip = ''.join(str(ip[0]))
                self.status[ip] = response
                if print_all:
                    print('[%s_State]:--%s--' % (ip, response))
                # TODO: Interval is too simplistic for multiple Tellos - only gets status from one Tello each interval
                time.sleep(interval)

            except socket.error as exc:
                print('[Exception_Error]Caught exception socket.error : %s' % exc)

    def get_log(self):
        return self.log
