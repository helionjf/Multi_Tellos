# -*- coding: utf-8 -*-
# Forked from https://github.com/TelloSDK/Multi-Tello-Formation
# This fork hosted at https://github.com/scubyd/Multi-Tello-Formation to support Python 3
# Updated and tested with Python 3.7

import sys
import queue
import time
import os
import threading
from tello_manager import TelloManager


def create_execution_pools(num):
    pools = []
    for _ in range(num):
        execution_pool = queue.Queue()
        pools.append(execution_pool)
    return pools


def drone_handler(tello, drone_queue):
    while True:
        while drone_queue.empty():
            pass
        next_command = drone_queue.get()
        tello.send_command(next_command)


def all_queue_empty(execution_pools):
    for pool in execution_pools:
        if not pool.empty():
            return False
    return True


def all_got_response(manager):
    for log in manager.get_log().values():
        if not log[-1].got_response():
            return False
    return True


def save_log(manager):
    log = manager.get_log()

    if not os.path.exists('log'):
        try:
            os.makedirs('log')
        except OSError as e:
            pass

    out = open('log/' + start_time + '.txt', 'w')
    cnt = 1
    for stat_list in log.values():
        out.write('------\nDrone: %s\n' % cnt)
        cnt += 1
        for stat in stat_list:
            out.write(stat.return_stats())
        out.write('\n')


def check_timeout(start_time, end_time, timeout):
    diff = end_time - start_time
    time.sleep(0.1)
    return diff > timeout


#
# Entry point of script!
#

manager = TelloManager()
start_time = str(time.strftime("%a-%d-%b-%Y_%H-%M-%S-%Z", time.localtime(time.time())))

try:
    file_name = sys.argv[1]
    f = open(file_name, "r")
    commands = f.readlines()

    tello_list = []
    execution_pools = []
    sn_ip_dict = {}
    id_sn_dict = {}
    ip_fid_dict = {}

    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            # Lines with comments are ignored
            if '//' in command:
                # ignore comments
                continue

            # scan is used to search for and add Tellos for later use
            elif 'scan' in command:
                num_of_tello = int(command.partition('scan')[2])

                manager.find_available_tello(num_of_tello)
                tello_list = manager.get_tello_list()
                execution_pools = create_execution_pools(num_of_tello)

                for tello_num in range(len(tello_list)):
                    t1 = threading.Thread(target=drone_handler, args=(tello_list[tello_num],
                                                                      execution_pools[tello_num]))
                    ip_fid_dict[tello_list[tello_num].tello_ip] = tello_num
                    t1.daemon = True
                    t1.start()

            # Enable Status message output, printing each status message
            elif 'print_status' in command:
                interval = float(command.partition('print_status')[2])
                manager.enable_status(interval, True)

            # Enable Status message output, without printing statuses
            elif 'status' in command:
                interval = float(command.partition('status')[2])
                manager.enable_status(interval, False)

            # Handle sending commands, for either all Tellos (for *>) or a single Tello (with 1>, 2>, etc)
            elif '>' in command:
                id_list = []
                tello_num = command.partition('>')[0]
                if tello_num == '*':
                    for x in range(len(tello_list)):
                        id_list.append(x)
                else:
                    id_list.append(int(tello_num)-1)
                action = str(command.partition('>')[2])

                # Push command to pools, i.e. add the command to the queue, ready to send
                # Need to translate from Tello Number (1, 2, etc) to its fid, reflecting the order Tellos were found
                # TODO: Check whether FID and tello_num / tello_id are the same!?
                for tello_id in id_list:
                    tello_sn = id_sn_dict[tello_id]
                    tello_ip = sn_ip_dict[tello_sn]
                    fid = ip_fid_dict[tello_ip]
                    execution_pools[fid].put(action)

            # Get battery levels and check that all Tellos have sufficient power
            elif 'battery_check' in command:
                
                threshold = int(command.partition('battery_check')[2])
                for queue in execution_pools:
                    queue.put('battery?')

                # Wait until all commands are executed
                while not all_queue_empty(execution_pools):
                    time.sleep(0.1)

                # Until all responses are received
                while not all_got_response(manager):
                    time.sleep(0.1)

                for tello_log in manager.get_log().values():
                    battery = int(tello_log[-1].response)
                    print('[Battery_Status]---IP:%s ----Battery Status: %d' % (tello_log[-1].drone_ip, battery))
                    if battery < threshold:
                        print('[Battery_Low]IP:%s ----Battery Below Threshold, Exiting!' % tello_log[-1].drone_ip)
                        save_log(manager)
                        exit(0)

                print('[Battery_Ok]Passed battery check!')

            # Incorporate a delay between commands
            elif 'delay' in command:
                delay_time = float(command.partition('delay')[2])
                print('[Delay_Seconds]Delaying for %fs' % delay_time)
                time.sleep(delay_time)

            # Used to associate serial numbers with IP addresses
            elif 'correct_ip' in command:

                for queue in execution_pools:
                    queue.put('sn?')

                # Wait until all commands are executed
                while not all_queue_empty(execution_pools):
                    time.sleep(0.1)

                # Until all responses are received
                while not all_got_response(manager):
                    time.sleep(0.1)

                for tello_log in manager.get_log().values():
                    tello_sn = str(tello_log[-1].response)
                    tello_ip = str(tello_log[-1].drone_ip)
                    sn_ip_dict[tello_sn] = tello_ip

            # Used to associate a specific Tello with a number, via its serial number
            elif '=' in command:
                drone_num = int(command.partition('=')[0])
                drone_sn = command.partition('=')[2]
                id_sn_dict[drone_num-1] = drone_sn
                print('[IP_SN_FID]:IP:%s----SN:%s----Num:%d\n' % (sn_ip_dict[drone_sn], drone_sn, drone_num))

            # sync is used to force instruction execution to pause until all queued commands are done with a response
            elif 'sync' in command:
                timeout = float(command.partition('sync')[2])
                print('[Sync_And_Wait]Sync for %ss' % timeout)
                time.sleep(0.1)
                try:
                    start = time.time()
                    # Wait until all commands are executed
                    while not all_queue_empty(execution_pools):
                        now = time.time()
                        if check_timeout(start, now, timeout):
                            raise RuntimeError
                    print('[Sync_Commands_Sent]All queues empty and all commands sent')

                    # Wait until all responses are received
                    while not all_got_response(manager):
                        now = time.time()
                        if check_timeout(start, now, timeout):
                            raise RuntimeError
                    print('[Sync_Got_Responses]All response received')

                except RuntimeError:
                    print('[Quit_Sync]Fail Sync: Timeout exceeded!')

    # Wait until all commands are executed
    while not all_queue_empty(execution_pools):
        time.sleep(0.1)

    # Wait until all responses are received
    while not all_got_response(manager):
        time.sleep(0.1)

    save_log(manager)


except KeyboardInterrupt:
    print('[Quit_ALL]Multi_Tello_Task exception. Requesting all drones to land...')
    for ip in manager.tello_ip_list:
        manager.socket.sendto('land'.encode(), (ip, 8889))

    save_log(manager)
