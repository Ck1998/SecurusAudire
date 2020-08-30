from modules.audits.base_model import BaseTest
import nmap
import psutil


class NetworkScannerUsingPing(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_result = {}

    @staticmethod
    def get_system_ips():
        if_addrs = psutil.net_if_addrs()

        network_info = {}

        for interface_name, interface_addresses in if_addrs.items():
            network_info[interface_name] = {}
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_info[interface_name].update(
                        IP_Address=address.address,
                        Netmask=address.netmask,
                        Broadcast_IP=address.broadcast
                    )

        return network_info

    @staticmethod
    def calculate_cidr_value(netmask):
        cidr_value = 0
        netmask_split = netmask.split(".")

        if len(netmask_split) != 4:
            return None

        for subnet in netmask_split:
            binary_subnet = str(bin(int(subnet)))
            cidr_value += binary_subnet.count("1")

        return cidr_value

    def calculate_network_ip(self, network_info: dict):
        ip_address = network_info["IP_Address"]
        netmask = network_info["Netmask"]

        cidr_value = self.calculate_cidr_value(netmask=netmask)
        if not cidr_value:
            return None

        if netmask.split(".").count("255") == 1:
            # Class A IP
            network_ip = f"{ip_address.split('.')[0]}.0.0.0"
        elif netmask.split(".").count("255") == 2:
            # class B IP
            network_ip = f"{ip_address.split('.')[0]}.{ip_address.split('.')[1]}.0.0"
        elif netmask.split(".").count("255") == 3:
            # class C IP
            network_ip = f"{ip_address.split('.')[0]}.{ip_address.split('.')[1]}.{ip_address.split('.')[2]}.0"
        else:
            return None

        return f"{network_ip}/{cidr_value}"

    def run_test(self):
        ip_scanner = nmap.PortScanner()

        network_info = self.get_system_ips()
        for interface, interface_info in network_info.items():

            if not interface_info:
                continue

            if interface_info["IP_Address"] == "127.0.0.1":
                # local host
                continue

            network_ip = self.calculate_network_ip(
                network_info=interface_info
            )
            self.test_result[f"Network - {network_ip}"] = {}
            ip_scan_result = ip_scanner.scan(hosts=network_ip, arguments='-n -sP -PE -PA21,23,80,3389', sudo=True)
            self.test_result[f"Network - {network_ip}"]['Total number of hosts'] = ip_scan_result['nmap']['scanstats']['totalhosts']
            self.test_result[f"Network - {network_ip}"]['Hosts - Up'] = ip_scan_result['nmap']['scanstats']['uphosts']
            self.test_result[f"Network - {network_ip}"]['Hosts - Down'] = ip_scan_result['nmap']['scanstats']['downhosts']

            self.test_result[f"Network - {network_ip}"]["Live Hosts"] = []

            for live_host in ip_scan_result['scan'].keys():
                self.test_result[f"Network - {network_ip}"]["Live Hosts"].append(live_host)

        return self.test_result
