from modules.audits.base_model import BaseTest
import nmap


class IPScannerUsingPing(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_result = {
            "Total number of hosts": "",
            "Hosts - Up": "",
            "Hosts - Down": "",
            "Live Hosts": []
        }

    def run_test(self):
        ip_scanner = nmap.PortScanner()
        ip_scan_result = ip_scanner.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389', sudo=True)

        self.test_result['Total number of hosts'] = ip_scan_result['nmap']['scanstats']['totalhosts']
        self.test_result['Hosts - Up'] = ip_scan_result['nmap']['scanstats']['uphosts']
        self.test_result['Hosts - Down'] = ip_scan_result['nmap']['scanstats']['downhosts']

        for live_host in ip_scan_result['scan'].keys():
            self.test_result["Live Hosts"].append(live_host)

        return self.test_result
