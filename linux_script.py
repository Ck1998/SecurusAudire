#!/usr/bin/env python3 

__author__ = "Chetanya Kunndra"

# imports

import sys
import time
import os

from time import sleep
from subprocess import check_output
import logging

import psutil
import platform
import os
import sys


# new imports
from utils.lib_general_utils import Util

# TODO: create classes for the function
log_file = open("Log_File.log", "w+")

# ------------------------------- Score Variable -------------------------------- #

score = 0


# ------------------------------- Score Variable -------------------------------- #


# =============================================================================== #
#                                                                                 #
#                      Formatting Functions and Variables                         #
#                                                                                 #
# =============================================================================== #

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


TAB_6 = "\t\t\t\t\t\t"


# =============================================================================== #
#                                                                                 #
#                    Formatting Functions and Variables Ends                      #
#                                                                                 #
# =============================================================================== #

# =============================================================================== #
#                                                                                 #
#                      1.0 General System Information Modules                     #
#                                                                                 #
# =============================================================================== #

def get_time_from_ntp_server():
    c = ntplib.NTPClient()

    for i in range(1, 3):
        try:
            response = c.request('in.pool.ntp.org', version=i)
            break;
        except:
            pass;

    response.offset

    return (datetime.fromtimestamp(response.tx_time, timezone.utc))


def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)

    log_file.write(
        "                        Boot Time: {}/{}/{} {}:{}:{}                     \n".format(bt.year, bt.month, bt.day,
                                                                                             bt.hour, bt.minute,
                                                                                             bt.second))


def get_system_information():
    # log_file = open("Log_File.log", "a+")

    sys_info = platform.uname()

    log_file.write("                           System: {}                          \n".format(sys_info.system))
    log_file.write("                        Node Name: {}                          \n".format(sys_info.node))
    log_file.write("                          Release: {}                          \n".format(sys_info.release))
    log_file.write("                          Version: {}                          \n".format(sys_info.version))
    log_file.write("                          Machine: {}                          \n".format(sys_info.machine))
    log_file.write("                        Processor: {}                          \n".format(sys_info.processor))

    # log_file.close()


def get_cpu_info():
    log_file.write(TAB_6 + "Physical cores: {}\n".format(psutil.cpu_count(logical=False)))
    log_file.write(TAB_6 + "Total cores: {}\n".format(psutil.cpu_count(logical=True)))

    cpufreq = psutil.cpu_freq()

    log_file.write(TAB_6 + f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    log_file.write(TAB_6 + f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    log_file.write(TAB_6 + f"Current Frequency: {cpufreq.current:.2f}Mhz\n")

    log_file.write("\n")
    log_file.write("\t\t\t\t\t\tCPU Usage Per Core:\n")
    log_file.write("\n")

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        log_file.write(TAB_6 + "\tCore {}: {}%\n".format(i, percentage))

    log_file.write("\n")
    log_file.write(TAB_6 + "Total CPU Usage: {}%\n".format(psutil.cpu_percent()))


def get_memory_info():
    svmem = psutil.virtual_memory()
    log_file.write(f"Total: {get_size(svmem.total)}\n")
    log_file.write(f"Available: {get_size(svmem.available)}\n")
    log_file.write(f"Used: {get_size(svmem.used)}\n")
    log_file.write(f"Percentage: {svmem.percent}%\n")


def get_swap_info():
    swap = psutil.swap_memory()
    log_file.write(f"Total: {get_size(swap.total)}\n")
    log_file.write(f"Free: {get_size(swap.free)}\n")
    log_file.write(f"Used: {get_size(swap.used)}\n")
    log_file.write(f"Percentage: {swap.percent}%\n")


def get_disk_info():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        log_file.write("\n")
        log_file.write("Device: {}\n".format(partition.device))
        log_file.write("  Mountpoint: {}\n".format(partition.mountpoint))
        log_file.write("  File system type: {}\n".format(partition.fstype))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        log_file.write("  Total Size: {}\n".format(get_size(partition_usage.total)))
        log_file.write("  Used: {}\n".format(get_size(partition_usage.used)))
        log_file.write("  Free: {}\n".format(get_size(partition_usage.free)))
        log_file.write("  Percentage: {}%\n".format(partition_usage.percent))

    log_file.write("\n")
    disk_io = psutil.disk_io_counters()
    log_file.write("Total read (Since Boot): {}\n".format(get_size(disk_io.read_bytes)))
    log_file.write("Total write (Since Boot): {}\n".format(get_size(disk_io.write_bytes)))


def get_network_info():
    if_addrs = psutil.net_if_addrs()

    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            log_file.write(f"=== Interface: {interface_name} ===\n")
            if str(address.family) == 'AddressFamily.AF_INET':
                log_file.write(f"  IP Address: {address.address}\n")
                log_file.write(f"  Netmask: {address.netmask}\n")
                log_file.write(f"  Broadcast IP: {address.broadcast}\n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                log_file.write(f"  MAC Address: {address.address}\n")
                log_file.write(f"  Netmask: {address.netmask}\n")
                log_file.write(f"  Broadcast MAC: {address.broadcast}\n")

    net_io = psutil.net_io_counters()
    log_file.write("\n")
    log_file.write(f"Total Bytes Sent (Since Boot): {get_size(net_io.bytes_sent)}\n")
    log_file.write(f"Total Bytes Received (Since Boot): {get_size(net_io.bytes_recv)}\n")


def get_local_password_policy():
    log_file.write("\n")

    out = check_output(["net", "accounts"])
    out = out.decode("utf-8")

    for line in out.split("\n"):
        if line == "The command completed successfully.\r":
            break
        else:
            log_file.write(line)


def get_grouo_info_policy():
    log_file.write("\n")

    out = check_output(["gpresult", "/Z"])
    out = out.decode("utf-8")

    for line in out.split("\n"):
        if line == "The command completed successfully.\r":
            break
        else:
            log_file.write(line)


# =============================================================================== #
#                                                                                 #
#                    1.0 General System Information Modules Ends                  #
#                                                                                 #
# =============================================================================== #

def main():
    # log_file = open("Log_File.log", "w+")

    ts = datetime.now()
    print(ts.strftime("%d-%m-%Y %H:%M:%S"))
    print(get_time_from_ntp_server())

    log_file.write("# ===================================================================================== #\n")
    log_file.write("#                                                                                       #\n")
    log_file.write("#                         SecurusAudire: A Security Audit Tool                          #\n")
    log_file.write("#                                  Version: 1.0beta                                     #\n")
    log_file.write("#                                                                                       #\n")
    log_file.write("# ===================================================================================== #\n")
    log_file.write("                                                               \n")
    log_file.write("                                                               \n")
    log_file.write("                                                               \n")
    log_file.write("                                                               \n")

    log_file.write("( -------------------------------------------------------------------------------------- )\n")
    log_file.write("(                           1.0 Genral System Information                                )\n")
    log_file.write("( -------------------------------------------------------------------------------------- )\n")

    log_file.write("\n")
    log_file.write("\n")

    log_file.write("( --------------------------- 1.1 Timestamp Information -------------------------------- )\n")
    log_file.write("\n")
    log_file.write(
        "                   Current System Time: {}                     \n".format(ts.strftime("%d-%m-%Y %H:%M:%S")))
    log_file.write(
        "         Timestamp from Time Server 'in.pool.ntp.org': {}      \n".format(get_time_from_ntp_server()))

    log_file.write("\n")
    log_file.write("\n")

    log_file.write("( --------------------------- 1.2 System Information -------------------------------- )\n")

    log_file.write("\n")

    get_system_information()

    log_file.write("\n")

    log_file.write("( ------------------------------- 1.3 Boot Time ------------------------------------ )\n")

    log_file.write("\n")

    get_boot_time()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.4 CPU Information --------------------------------- )\n")

    log_file.write("\n")

    get_cpu_info()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.5 Memory Information --------------------------------- )\n")

    log_file.write("\n")

    get_memory_info()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.6 SWAP Information --------------------------------- )\n")

    log_file.write("\n")

    log_file.write(
        "( INFORMATION: A swap file (or swap space or, in Windows NT, a pagefile) is a space on a\nhard disk used as the virtual memory extension of a computer's real memory (RAM). Having a\nswap file allows your computer's operating system to pretend that you have more RAM than\nyou actually do )\n")

    log_file.write("\n")

    get_swap_info()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.7 Disk Information --------------------------------- )\n")

    get_disk_info()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.8 Network Information --------------------------------- )\n")

    get_network_info()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.10 Local Password Policy --------------------------------- )\n")

    get_local_password_policy()

    log_file.write("\n")

    log_file.write("( ---------------------------- 1.10 Group Policy Information --------------------------------- )\n")

    get_grouo_info_policy()

    log_file.write("\n")
    log_file.write("\n")

    log_file.write("( -------------------------------------------------------------------------------------- )\n")
    log_file.write("(                               2.0 Group Management                                     )\n")
    log_file.write("( -------------------------------------------------------------------------------------- )\n")

    log_file.write("\n")
    log_file.write("\n")

    log_file.close()


main()
