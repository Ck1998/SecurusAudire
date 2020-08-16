import psutil
import platform
from modules.audits.base_model import BaseTest


class GeneralSystemInformation(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_results = {}

    def get_boot_time(self):
        self.test_results['Boot Time'] = {}
        boot_time_timestamp = psutil.boot_time()
        bt = self.util_obj.get_datetime_fromtimestamp(boot_time_timestamp)
        self.test_results['Boot Time']["Boot Time"] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

    def get_system_information(self):
        sys_info = platform.uname()
        self.test_results["System Information"] = {
            "System": sys_info.system,
            "Node_Name": sys_info.node,
            "Release": sys_info.release,
            "Version": sys_info.version,
            "Machine": sys_info.machine,
            "Processor": sys_info.processor
        }

    def get_cpu_info(self):

        cpufreq = psutil.cpu_freq()

        self.test_results["CPU Information"] = {
            "Physical_Cores": psutil.cpu_count(logical=False),
            "Total_Cores": psutil.cpu_count(logical=True),
            "Max_Frequency": f"{cpufreq.max:.2f}Mhz",
            "Min_Frequency": f"{cpufreq.min:.2f}Mhz",
            "Current_Frequency": f"{cpufreq.current:.2f}Mhz",
            "CPU_Usage_Per_Core": {},
            "Total_CPU_Usage": f"{psutil.cpu_percent()} %"
        }

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            core_name = f"Core {i}"
            self.test_results["CPU Information"]['CPU_Usage_Per_Core'][core_name] = f"{percentage} %"

    def get_memory_info(self):
        svmem = psutil.virtual_memory()
        self.test_results["Memory Information"] = {}
        self.test_results["Memory Information"] = {
            "Total": self.util_obj.get_size(svmem.total),
            "Available": self.util_obj.get_size(svmem.available),
            "Used": self.util_obj.get_size(svmem.used),
            "Percentage": f"{self.util_obj.get_size(svmem.percent)} %"
        }

    def get_swap_info(self):
        swap = psutil.swap_memory()
        self.test_results["Swap Information"] = {}
        self.test_results["Swap Information"] = {
            "Total": self.util_obj.get_size(swap.total),
            "Free": self.util_obj.get_size(swap.free),
            "Used": self.util_obj.get_size(swap.used),
            "Percentage": f"{self.util_obj.get_size(swap.percent)} %"
        }

    def get_disk_info(self):
        partitions = psutil.disk_partitions()
        self.test_results["Disk Information"] = {}
        for partition in partitions:
            self.test_results["Disk Information"][partition.device] = {}
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            self.test_results["Disk Information"][partition.device].update(
                Mountpoint=partition.mountpoint,
                File_System_Type=partition.fstype,
                Total_Size=self.util_obj.get_size(partition_usage.total),
                Used=self.util_obj.get_size(partition_usage.used),
                Free=self.util_obj.get_size(partition_usage.free),
                Percentage=f"{partition_usage.percent} %"
            )

        disk_io = psutil.disk_io_counters()

        self.test_results["Disk Information"]["Total read (Since Boot)"] = self.util_obj.get_size(
            disk_io.read_bytes)
        self.test_results["Disk Information"]["Total write (Since Boot)"] = self.util_obj.get_size(
            disk_io.write_bytes)

    def get_network_info(self):
        if_addrs = psutil.net_if_addrs()

        self.test_results["Network Information"] = {}

        for interface_name, interface_addresses in if_addrs.items():

            self.test_results["Network Information"][interface_name] = {}

            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    self.test_results["Network Information"][interface_name].update(
                        IP_Address=address.address,
                        Netmask=address.netmask,
                        Broadcast_IP=address.broadcast
                    )
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    self.test_results["Network Information"][interface_name].update(
                        MAC_Address=address.address,
                        Netmask=address.netmask,
                        Broadcast_MAC=address.broadcast
                    )

        net_io = psutil.net_io_counters()

        self.test_results["Network Information"]["Total Bytes Sent (Since Boot)"] = self.util_obj.get_size(
            net_io.bytes_sent)
        self.test_results["Network Information"]["Total Bytes Received (Since Boot)"] = self.util_obj.get_size(
            net_io.bytes_recv)

    def run_all_functions(self):
        self.get_boot_time()
        self.get_system_information()
        self.get_cpu_info()
        self.get_memory_info()
        self.get_swap_info()
        self.get_disk_info()
        self.get_network_info()

    def run_test(self):
        self.run_all_functions()
        return self.test_results
