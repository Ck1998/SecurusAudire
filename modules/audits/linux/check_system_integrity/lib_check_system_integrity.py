from modules.audits.base_model import BaseTest
import config as CONFIG


class CheckSystemIntegrity(BaseTest):
    
    def __init__(self):
        super().__init__()
        self.test_result = {}

    def check_SIP_status(self):
        sip_service_status = self.util_obj.get_command_output([self.ROOT_DIR+"usr/bin/csrutil", "status"])
        
        self.test_result['System Integrity Protection Status'] = {}

        if 'enabled' in sip_service_status:
            CONFIG.SYSTEM_SCORE += 1
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            self.test_result['System Integrity Protection Status'].update(result = "SIP enabled", args = None)
        else:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.SUGGESTIONS_DICT["System Integrity Protection"] = {
                "Suggestion": "Enable CSrutil for added system protection",
                "Support Link": "https://www.capatek-tutorials.com/osx/how-to-disable-and-enable-system-integrity-protection-in-mac-osx-10-11/"
            }
            self.test_result['System Integrity Protection Status'].update(result = "SIP Disabled", args = None)

    def check_csrutil(self):
        csrutils_file_path = self.ROOT_DIR+"usr/bin/csrutil"
        self.test_result['Checking for CSrutil'] = {}
        result = self.util_obj.check_file_exsists(csrutils_file_path)
        
        if result:
            self.test_result['Checking for CSrutil'].update(result = "CSrutil binary found.", args = None)
            CONFIG.SYSTEM_SCORE += 1
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            self.check_SIP_status()
        else:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.SUGGESTIONS_DICT["CSrutil"] = {
                "Suggestion": "Install CSrutil for added system protection",
                "Support Link": "https://www.unix.com/man-page/mojave/8/csrutil/"
            }
            self.test_result['Checking for CSrutil'].update(result = "No CSrutil binary found. Skipping additonal tests.", args = None)

    def run_test(self):
        self.check_csrutil()
        return self.test_result
