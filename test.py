import json

from modules.lib_test_home_dir import TestHomeDir
from modules.lib_check_system_integrity import CheckSystemIntegrity
from modules.lib_kernel_hardening import KernelHardening
from modules.lib_check_root_kit import CheckRootKits
from modules.general_system_information import GeneralSystemInformation
from modules.lib_authentication import CheckAuthenticationModule
from generate_web_report import GenerateWebReport


obj = TestHomeDir()
obj2 = CheckRootKits()
obj3 = CheckSystemIntegrity()
obj4 = KernelHardening()
obj5 = GeneralSystemInformation()
obj6 = CheckAuthenticationModule()
data = {
    "authentication": obj6.run_test(),
    "General System information": obj5.run_test(),
    "Check Root Kit": obj2.run_test(),
    "Check Home Dir": obj.run_test(),
    "Check System Integrity": obj3.run_test(),
    "Kernel Hardening": obj4.run_test()
}

web = GenerateWebReport(data)
web.generate_report()

print(json.dumps(data)) 