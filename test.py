import json

from modules.lib_test_home_dir import TestHomeDir
from modules.lib_check_system_integrity import CheckSystemIntegrity
from modules.check_root_kit.lib_check_root_kit import CheckRootKits

obj = TestHomeDir()
obj2 = CheckRootKits()
obj3 = CheckSystemIntegrity()
data = {
    "Check Root Kit": obj2.run_test(),
    "Check Home Dir": obj.run_test(),
    "Check System Integrity": obj3.run_test() 
}

print(json.dumps(data))