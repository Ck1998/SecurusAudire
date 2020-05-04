from modules.audit_controller import AuditController
from config import CURR_SYSTEM_PLATFORM, ROOT_DIR

# UAC elevation
import ctypes
import sys


class SecurusAudireCLI:

    def __init__(self):
        super().__init__()
        self.save_folder_location = ""

    def run_audit(self):
        audit_controller_object = AuditController(self.save_folder_location)
        audit_status = audit_controller_object.controller()
        
        if audit_status == 5:
            print("OS not supported")
        elif audit_status == 0:
            print('System Audit Complete. You can view generated reports at - '+self.save_folder_location+"/SecurusAudire_Reports/")
        else:
            answer = input('SecurusAudire encountered some errors, are you running the script as root?') 
            if 'n' in answer.lower():
                print('Script should be executed with root privileges!!!')
            else:
                print('Please exit and try again!!!')

    def run_cli(self):
        self.save_folder_location = input("Enter location to save generated reports (default: /var/log/SecurusAudire_Reports)- ")

        if len(self.save_folder_location) == 0:
            
            if CURR_SYSTEM_PLATFORM == "linux":
                
                self.save_folder_location = "/var/log"

            elif CURR_SYSTEM_PLATFORM == "windows":
                
                self.save_folder_location = ROOT_DIR

        if CURR_SYSTEM_PLATFORM == "windows":
            self.save_folder_location = self.save_folder_location.replace("/", '\\')

        self.run_audit()


def is_admin():
    try: 
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":

    if CURR_SYSTEM_PLATFORM == "windows":
        
        if is_admin():
            # check if user is admin, if True then run audit
            # else re run program with admin privledges
            cli_obj = SecurusAudireCLI()
            cli_obj.run_gui()

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    elif CURR_SYSTEM_PLATFORM == "linux":
        cli_obj = SecurusAudireCLI()
        cli_obj.run_cli()
