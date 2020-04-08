from modules.lib_test_home_dir import TestHomeDir
from modules.lib_check_system_integrity import CheckSystemIntegrity
from modules.lib_kernel_hardening import KernelHardening
from modules.lib_check_root_kit import CheckRootKits
from modules.general_system_information import GeneralSystemInformation
from modules.lib_authentication import CheckAuthenticationModule
from generate_web_report import GenerateWebReport


class AuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_results = {}

    def run_all_audits(self):

        test_home_dir_object = TestHomeDir()
        check_root_kits_object = CheckRootKits()
        check_system_integrity_object = CheckSystemIntegrity()
        kernel_hardening_object = KernelHardening()
        general_system_info_object = GeneralSystemInformation()
        check_authentication_object = CheckAuthenticationModule()

        self.audit_results = {
            "General System information": general_system_info_object.run_test(),
            "authentication": check_authentication_object.run_test(),
            "Check Home Dir": test_home_dir_object.run_test(),
            "Check System Integrity": check_system_integrity_object.run_test(),
            "Kernel Hardening": kernel_hardening_object.run_test(),
            "Check Root Kit": check_root_kits_object.run_test()
        }

        self.generate_log_report()
        self.generate_web_report()

    def generate_web_report(self):
        web = GenerateWebReport(self.audit_results, self.save_folder_location)
        web.generate_report()

    def generate_log_report(self):
        #web = GenerateWebReport(self.audit_results, self.save_folder_location)
        #web.generate_report()
        pass

    def controller(self):
        try:
            self.run_all_audits()
        except:
            return 1

        return 0 