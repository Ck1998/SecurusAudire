# common audit modules
from modules.audits.common import *

# linux Audit modules
from modules.audits.linux import *

from modules.audits.base_model import BaseTest

# report modules
from modules.report_generation.report_generation_controller import ReportGenController

# config variable
import config as CONFIG

# debugging module
from traceback import print_exc

# timestamp modules
from datetime import datetime

# Regex module
import re


class LinuxAuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = {}
        self.full_report = {}
        self.audit_start_time = ""
        self.audit_end_time = ""

    @staticmethod
    def fetch_all_audit_classes():
        audit_classes = BaseTest.__subclasses__()
        return audit_classes

    def run_all_audits(self):
        audit_classes = self.fetch_all_audit_classes()
        """test_home_dir_object = TestHomeDir()
        check_root_kits_object = CheckRootKits()
        check_system_integrity_object = CheckSystemIntegrity()
        kernel_hardening_object = KernelHardening()
        general_system_info_object = GeneralSystemInformation()
        check_authentication_object = CheckAuthenticationModule()
        check_memory_processes = CheckMemoryProcesses()"""

        for audit_class in audit_classes:
            if audit_class.__disabled__:
                continue
            else:
                audit_name = re.sub(r"(\w)([A-Z])", r"\1 \2", audit_class.__name__)
                self.audit_result[audit_name] = audit_class().run_test()

        """self.audit_result = {
            "General System Information": general_system_info_object.run_test(),
            "Authentication Audits": check_authentication_object.run_test(),
            "Home Directory Audits": test_home_dir_object.run_test(),
            "Memory Process Audits": check_memory_processes.run_test(),
            "System Integrity Audits": check_system_integrity_object.run_test(),
            "Kernel Hardening Audits": kernel_hardening_object.run_test(),
            "Root Kit Audits": check_root_kits_object.run_test()
        }"""

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
        except:
            print(print_exc())
            return 1
            
        return 0


# TODO: Change reports
