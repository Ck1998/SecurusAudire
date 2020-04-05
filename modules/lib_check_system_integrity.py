from modules.base_model import BaseTest
from config import ROOT_DIR

class CheckSystemIntegrity(BaseTest):
    
    def __init__(self):
        super().__init__()
        self.test_result = {}

    def check_SIP_status(self):
        sip_service_status = self.util_obj.get_command_output([ROOT_DIR+"usr/bin/csrutil", "status"])
        
        self.test_result['System Integrity Protection Status'] = {}

        if 'enabled' in sip_service_status:
            self.test_result['System Integrity Protection Status'].update(result = "SIP enabled", args = None)
        else:
            self.test_result['System Integrity Protection Status'].update(result = "SIP Disabled", args = None)

    def check_csrutil(self):
        csrutils_file_path = ROOT_DIR+"usr/bin/csrutil"
        self.test_result['Checking for CSrutil'] = {}
        result = self.util_obj.check_file_exsists(csrutils_file_path)
        
        if result:
            self.test_result['Checking for CSrutil'].update(result = "CSrutil binary found.", args = None)
        else:
            self.test_result['Checking for CSrutil'].update(result = "No CSrutil binary found. Skipping additonal tests.", args = None)

    
    def run_test(self):
        self.check_csrutil()
        return self.test_result
