# add audit modules
from modules.audits.windows.windows_registry_check.lib_windows_registry_check import WindowsRegistryAudits
from modules.audits.common.general_system_information.lib_general_system_information import GeneralSystemInformation

# report modules
from modules.report_generation.report_generation_controller import ReportGenController

# config varibales
import config as CONFIG

# debugging module 
from traceback import print_exc

# datetime module
from datetime import datetime


class WindowsAuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = {}
        self.full_report = {}
        self.audit_start_time = ""
        self.audit_end_time = ""

    def run_all_audits(self):

        windows_registry_audits_object = WindowsRegistryAudits()
        general_system_info_object = GeneralSystemInformation()

        self.audit_result = {
            "General System Information": general_system_info_object.run_test(),
            "Windows Registry Audits": windows_registry_audits_object.run_test()
        }

        self.generate_full_report()

    def generate_full_report(self):

        # this function is used for adding audit score and warnings and suggwstions to the audit_results

        self.audit_end_time = datetime.now()
        
        self.full_report = {
            "System Score": CONFIG.SYSTEM_SCORE,
            "Total Score Possible": CONFIG.TOTAL_SCORE_POSSIBLE,
            'Audit Start Time': str(self.audit_start_time),
            'Audit End Time': str(self.audit_end_time),
            'Audit Duration': str(self.audit_end_time - self.audit_start_time),
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
            self.audit_start_time = datetime.now()
            self.run_all_audits()

        except Exception:
            print(print_exc())
            return 1
            
        return 0 