import traceback

# audit modules
from modules.audits.windows.win_reg import WindowsRegistryAudits

from modules.audits.common.general_system_information.lib_general_system_information import GeneralSystemInformation

# report modules
from modules.report_generation.report_generation_controller import ReportGenController

# config varibales
import config as CONFIG


class AuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = {}
        self.full_report = {}

    def run_all_audits(self):

        obj = WindowsRegistryAudits()
        obj2= GeneralSystemInformation()

        self.audit_result = {
            "General System information": obj2.run_test(),
            "Winreg": obj.run_test()
        }

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
        except Exception as e:
            print(traceback.print_exc())
            return 1
            
        return 0 