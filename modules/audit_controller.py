# audit modules
from modules.audits.linux.check_authentication.lib_authentication import CheckAuthenticationModule
from modules.audits.linux.check_system_integrity.lib_check_system_integrity import CheckSystemIntegrity
from modules.audits.linux.kernel_hardening.lib_kernel_hardening import KernelHardening
from modules.audits.linux.check_root_kit.lib_check_root_kit import CheckRootKits
from modules.audits.linux.test_home_dir.lib_test_home_dir import TestHomeDir
from modules.audits.common.general_system_information.lib_general_system_information import GeneralSystemInformation

# report modules
from modules.report_generation.report_generation_controller import ReportGenController


class AuditController:

    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = {}

    def run_all_audits(self):

        test_home_dir_object = TestHomeDir()
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
        }

        self.generate_reports()

    def generate_reports(self):
        report_gen_obj = ReportGenController(self.audit_result, self.save_folder_location)

        report_gen_obj.controller()

    def controller(self):
        try:
            self.run_all_audits()
        except:
            return 1

        return 0 