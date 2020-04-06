from datetime import datetime, timezone
from ntplib import NTPClient
from subprocess import check_output
import os
import re
import glob
from config import LOG_FILE

class Utils:
    
    """
        This class contains all the util functions requireed by the code
    """
    
    def __init__(self):
        super().__init__()
        
        # constants
        self.NEW_LINE_1 = "\n"
        self.NEW_LINE_2 = "\n\n"
        self.NEW_LINE_3 = "\n\n\n"
        self.NEW_LINE_4 = "\n\n\n\n"
        self.NEW_LINE_5 = "\n\n\n\n\n"
        self.NEW_LINE_6 = "\n\n\n\n\n\n"
        self.TAB_6 = "\t\t\t\t\t\t"
        self.TAB_5 = "\t\t\t\t\t"
        self.TAB_4 = "\t\t\t\t"
        self.TAB_3 = "\t\t\t"
        self.TAB_2 = "\t\t"
        self.TAB_1 = "\t"
        
    @staticmethod
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    @staticmethod
    def get_time_from_ntp_server():
        c = NTPClient()

        for i in range(1, 3):
            try:
                response = c.request('in.pool.ntp.org', version=i)
                break
            except:
                pass

        response.offset

        return (datetime.fromtimestamp(response.tx_time, timezone.utc))
    
    @staticmethod
    def get_current_datetime():
        curr_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if curr_datetime is None:
            raise EnvironmentError
        else:
            return curr_datetime
    
    @staticmethod
    def get_datetime_fromtimestamp(timestamp):
        formatted_datetime = datetime.fromtimestamp(timestamp)

        return formatted_datetime
    
    @staticmethod
    def write_line_to_log_file(line_to_write: str):
        with open(LOG_FILE+".log", "a+") as write_file_object:
            try:
                write_file_object.write(line_to_write+NEW_LINE_1)
                return 0
            except:
                raise IOError

    @staticmethod
    def check_file_exsists(file_path: str):
        result = os.path.exists(file_path)
        return result

    @staticmethod
    def check_is_file(file_path: str):
        result = os.path.isfile(file_path)
    
        return result

    @staticmethod
    def recursive_search(file_path: str, file_name: str):
        file_list = []
        for filename in glob.iglob(file_path+'**/'+file_name, recursive = True): 
            file_list.append(filename)

        return file_list
    
    @staticmethod
    def get_command_output(args: list):
        command_output = check_output(args)
        command_output = command_output.decode('utf-8')

        return command_output

    @staticmethod
    def run_regex_finditer(regex: str, data: str):
        iter_obj = re.finditer(regex, data)
        
        return iter_obj

    @staticmethod
    def run_regex_search(regex: str, data: str):
        match = re.search(regex, data)
        
        return match

