# from modules.audits.base_model import BaseTest
from scapy import *
import socket
from subprocess import check_output, CalledProcessError
#from config import CURR_SYSTEM_PLATFORM
import json
import threading
from queue import Queue

class PortScanner:  # (BaseTest):

    def __init__(self, network_info: dict = None):
        super().__init__()
        self.connected_nodes_in_network = []
        self.connected_nodes_to_machine = []
        self.connected_nodes_in_network_info = {}
        self.connected_nodes_to_machine_info = {}
        self.all_possible_ips = {}
        self.system_network = {}
        self.network_info = network_info
        self.test_results = {}

    @staticmethod
    def get_port_status(ip, port, socket_object):
        try:
            print("checking "+port)
            connection_object = socket_object.connect((ip, port))
            connection_object.close()
            return True
        except:
            return False

    def multi_threading_control(self, ip, socket_object, queue_obj):
        active_port = []
        while True:
            port = queue_obj.get()
            result = self.get_port_status(ip=ip,
                                          port=port,
                                          socket_object=socket_object)
            if result:
                active_port.append(port)
            queue_obj.task_done()

        return active_port

    def scan_ports(self):

        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for interface in self.system_network.keys():
            socket_obj.bind((interface, 0))
            for ip in interface["connected_nodes"]:

                self.system_network[interface]["Open_Port_Analysis"][ip] = []
                queue_obj = Queue()

                for port in (1, 65535):
                    queue_obj.put(port)

                active_ports = self.multi_threading_control(ip = ip,
                                                           socket_object=socket_obj,
                                                           queue_obj=queue_obj)

                self.system_network[interface]["Open_Port_Analysis"][ip] = active_ports

            socket_obj.close()

    def run_test(self):
        self.scan_ports()
