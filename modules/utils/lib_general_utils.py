from datetime import datetime, timezone
from ntplib import NTPClient
from subprocess import check_output
import os
import re
import glob
from config import LOG_FILE
import json
from json2html import *

class Utils:
    
    """
        This class contains all the util functions requireed by the code
    """
    
    def __init__(self):
        super().__init__()

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

    @staticmethod
    def convert_dict_to_json(dict_convert: dict):
        try:
            converted_json = json.dumps(dict_convert, indent=4)
        except:
            converted_json = json.dumps({"None":"None"})

        return converted_json

    @staticmethod
    def convert_json_to_html_table(json_data: dict):
        minify_html_table = json2html.convert(json = json_data, table_attributes=f'class="table table-bordered table-hover"')

        return minify_html_table