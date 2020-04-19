# add audit modules
# report modules
from modules.report_generation.report_generation_controller import ReportGenController

# config varibales
import config as CONFIG

# debugging module 
from traceback import print_exc


class WindowsAuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = {}
        self.full_report = {}

    def run_all_audits(self):

        """test_home_dir_object = TestHomeDir()
        check_root_kits_object = CheckRootKits()
        check_system_integrity_object = CheckSystemIntegrity()
        kernel_hardening_object = KernelHardening()
        general_system_info_object = GeneralSystemInformation()
        check_authentication_object = CheckAuthenticationModule()

        self.audit_result = {
            "General System information": general_system_info_object.run_test(),
            "authentication": check_authentication_object.run_test(),
            "Check Home Dir": test_home_dir_object.run_test(),
            "Check System Integrity": check_system_integrity_object.run_test(),
            "Kernel Hardening": kernel_hardening_object.run_test(),
            "Check Root Kit": check_root_kits_object.run_test()
        }"""

        self.audit_result = {}

        self.generate_full_report()

    def generate_full_report(self):

        # this function is used for adding audit score and warnings and suggwstions to the audit_results

        self.full_report = {
            "System Score": CONFIG.SYSTEM_SCORE,
            "Total Score Possible": CONFIG.TOTAL_SCORE_POSSIBLE,
            "Suggestions": CONFIG.SUGGESTIONS_DICT,
            "Warnings": CONFIG.WARNING_DICT,
            "Audit Results": self.audit_result
        }

        self.generate_reports()

    def generate_reports(self):
        report_gen_obj = ReportGenController(self.full_report, self.save_folder_location)

        report_gen_obj.controller()

    def controller(self):
        try:
            self.run_all_audits()
        except Exception:
            print(print_exc())
            return 1
            
        return 0 