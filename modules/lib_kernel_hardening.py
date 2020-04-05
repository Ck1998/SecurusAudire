from modules.base_model import BaseTest
from config import ROOT_DIR

class KernelHardening(BaseTest):

    def __init__(self):
        super().__init__()
        self.sysctl_keys_regex = r"(.+)(?:[\s])=(?:[\s])(.+)"
        self.parse_db_regex = r"(.+)(?:[\s])@(?:[\s])(.*)(?:[\s])!(?:[\s])(.*)(?:[\s]):(?:[\s])(.*)(?:[\s]):(?:[\s])url:(.*)"
        self.db_location = "db/kernel_hardening_db.txt"

    def format_sysctl_keys(self, raw_keys: str):
        matches = self.util_obj.run_regex_finditer(self.sysctl_keys_regex, raw_keys)

        formatted_keys = {}

        for match in matches:
            formatted_keys[match.group(1)] = match.group(2)

        return formatted_keys

    def get_all_sysctl_keys(self):
        sysctl_keys_raw = self.util_obj.get_command_output(['sysctl', '-a'])

        sysctl_keys_formatted = self.format_sysctl_keys(sysctl_keys_raw)

        return sysctl_keys_formatted

    def check_sysctl_keys(self, db_dict: dict):
        
        # get system sysctl keys
        system_sysctl_keys = self.get_all_sysctl_keys()

        # checking against databse
    
    
    
    
    def parse_db(self):
        db_dict = {}
        with open(self.db_location, 'r') as db_read_obj:
            matches = self.util_obj.run_regex_finditer(self.parse_db_regex, db_read_obj.read())
            for match in matches:
                
                # keys to extract from the database
                # match.group(1) : sysctl (No use as of this now, just meant for reference purpose)
                # match.group(2) : sysctl key to check
                # match.group(3) : Expected value of that sysctl key 
                # match.group(4) : Decription of the sysctl key (if any)
                # match.group(5) : reference links (if any)
                
                db_dict[match.group(2)] = {}
                db_dict[match.group(2)].update(expected_value = match.group(3), description=match.group(4), support_link=match.group(5))
            
        self.check_sysctl_keys(db_dict)
    
    def run_test(self):
        pass