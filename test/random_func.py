import os
import sys
import glob
import re
from subprocess import check_output
# working
def get_env_variable():
    print(os.environ["PATH"].split(":"))

# working
def get_root_dir():
    ROOT_VARIABLE = '/' if os.path.abspath(sys.executable)[0] is None else os.path.abspath(sys.executable)[0]
    print(ROOT_VARIABLE)

# working
def check_file_exsists(file_path):
        result = os.path.exists(file_path)
        print(result)

# working
def glob_check(file_path,file_name):
    for filename in glob.iglob(file_path+'**/'+file_name, recursive = True): 
        print(filename) 

def check__name__():
    __name__ = "check__name__"
    print(__name__)

def check_regex(regex, file):
    with open(file, 'r') as rb:
        data = rb.read()
        match = re.search(regex, data) 
        if match:
            print("wow")
        else:
            print(":(")

def check_is_file(file_path):
        result = os.path.isfile(file_path)
        print(result)

def check_service():
    sip_service_status = check_output(["service","dbus", "status"])


check_service()