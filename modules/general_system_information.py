import psutil
from config import LOG_FILE
from datetime import datetime
from utils.lib_general_utils import Utils

class GeneralSystemInformation:
    
    def __init__(self):
        super().__init__()
        self.utils_obj = Utils()
        
    def get_boot_time(self):
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        self.utils_obj.write_line_to_log_file(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    
    def get_system_information(self):
        sys_info = platform.uname()
        
        line_to_write = f"System: {sys_info.system}"+self.utils_obj.NEW_LINE_1+     \
                        f"Node Name: {sys_info.node}"+self.utils_obj.NEW_LINE_1+    \
                        f"Release: {sys_info.release}"+self.utils_obj.NEW_LINE_1+   \
                        f"Version: {sys_info.version}"+self.utils_obj.NEW_LINE_1+   \
                        f"Machine: {sys_info.machine}"+self.utils_obj.NEW_LINE_1+   \
                        f"Processor: {sys_info.processor}"

        self.utils_obj.write_line_to_log_file(line_to_write)

    def get_cpu_info(self):
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


    def get_memory_info(self):
        svmem = psutil.virtual_memory()
        log_file.write(f"Total: {get_size(svmem.total)}\n")
        log_file.write(f"Available: {get_size(svmem.available)}\n")
        log_file.write(f"Used: {get_size(svmem.used)}\n")
        log_file.write(f"Percentage: {svmem.percent}%\n")


    def get_swap_info(self):
        swap = psutil.swap_memory()
        log_file.write(f"Total: {get_size(swap.total)}\n")
        log_file.write(f"Free: {get_size(swap.free)}\n")
        log_file.write(f"Used: {get_size(swap.used)}\n")
        log_file.write(f"Percentage: {swap.percent}%\n")


    def get_disk_info(self):
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


    def get_network_info(self):
        if_addrs = psutil.net_if_addrs()
        line_to_write = ""
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                line_to_write += (f"=== Interface: {interface_name} ===\n")
                if str(address.family) == 'AddressFamily.AF_INET':
                    line_to_write += (f"  IP Address: {address.address}\n")
                    line_to_write += (f"  Netmask: {address.netmask}\n")
                    line_to_write += (f"  Broadcast IP: {address.broadcast}\n")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    line_to_write += (f"  MAC Address: {address.address}\n")
                    line_to_write += (f"  Netmask: {address.netmask}\n")
                    line_to_write += (f"  Broadcast MAC: {address.broadcast}\n")

        net_io = psutil.net_io_counters()
        line_to_write += ("\n")
        line_to_write += (f"Total Bytes Sent (Since Boot): {self.utils_obj.get_size(net_io.bytes_sent)}\n")
        line_to_write += (f"Total Bytes Received (Since Boot): {self.utils_obj.get_size     (net_io.bytes_recv)}\n")