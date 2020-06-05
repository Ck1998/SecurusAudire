# from modules.audits.base_model import BaseTest
from subprocess import check_output, CalledProcessError
from concurrent.futures import ThreadPoolExecutor
import threading


class IPScannerUsingPing:  # (BaseTest):

    def __init__(self, all_possible_ips: list = None):
        super().__init__()
        self.all_possible_ips = all_possible_ips  # Set of 256 strings
        self.active_ips = []
        self.thread_pool_executor_obj = ThreadPoolExecutor(max_workers=32)

    """
        Ye karega ye saari ip lega 
        ek ek karke ping karega 
        check karega response ka agar 
        response aaya too active ip mai daal dega
        Isme ThreadPoolExecutor kaise use karun         
    """

    def send_ping_packet(self):
        for ip in self.all_possible_ips:
            output = ""
            try:
                # if CURR_SYSTEM_PLATFORM == "linux":
                output = check_output(["ping", "-c", "1", ip])
                # elif CURR_SYSTEM_PLATFORM == "windows":
                #    output = check_output(["ping", "-n", "3", ip])
            except CalledProcessError:
                continue

            output = output.decode("utf-8")
            if "100% packet loss" not in output:
                self.active_ips.append(ip)


    def run_test(self):
        #self.send_ping_packet()
        self.thread_pool_executor_obj.submit(self.send_ping_packet)
        return self.active_ips
