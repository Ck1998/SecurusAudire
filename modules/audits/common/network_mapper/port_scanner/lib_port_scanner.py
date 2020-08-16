import nmap
from modules.audits.base_model import BaseTest


class PortScanner(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_result = {}

    def run_test(self):
        port_scanner = nmap.PortScanner()
        ip_scan_result = port_scanner.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389', sudo=True)

        for live_host in ip_scan_result['scan'].keys():
            port_scanner_result = port_scanner.scan(live_host, sudo=True)
            self.test_result[live_host] = {}
            for port, port_res in port_scanner_result['scan'][live_host]['tcp'].items():
                self.test_result[live_host][port] = {
                    "State": port_res['state'],
                    "Name": port_res['name'],
                    "Product": port_res['product'],
                    "Version": port_res['version']
                }

        return self.test_result