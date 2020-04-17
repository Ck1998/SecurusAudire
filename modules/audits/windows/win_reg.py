from winreg import ConnectRegistry, EnumKey, HKEY_CLASSES_ROOT, HKEY_CURRENT_CONFIG
from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, OpenKeyEx
from winreg import CloseKey, EnumValue, KEY_READ, OpenKey, QueryValueEx

from modules.audits.base_model import BaseTest
import config as CONFIG


class WindowsRegistryAudits(BaseTest):

    def __init__(self):
        super().__init__()
        self.test_results = {}
        self.registry_key_regex = r"root_folder:(?:[\s])?(.+[^\s])(?:[\s])?->(?:[\s])?path:(?:[\s])?(.+[^\s])(?:[\s])?->(?:[\s])?sub_key:(?:[\s])?(.+[^\s])(?:[\s])?->(?:[\s])?expected_value:(?:[\s])?(.+[^\s])(?:[\s])?->(?:[\s])?desc:(?:[\s])?(.+[^\s])(?:[\s])?"


    def check_registry_key_exsists(self, root_folder: str, key_path: str, sub_key:str):

        if "hkey_local_machine" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

        elif "hkey_classes_root" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CLASSES_ROOT)

        elif "hkey_current_config" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CURRENT_CONFIG)

        elif "hkey_current_user" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CURRENT_USER)

        elif "heky_users" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_USERS)
            

        try:
            registry_key = OpenKey(root_folder, key_path)
            CloseKey(registry_key)
        except:
            # key not found 
            system_value = None

        

        return system_value


    def get_registry_key_value(self, root_folder: str, key_path: str, sub_key:str):
        
        if "hkey_local_machine" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

        elif "hkey_classes_root" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CLASSES_ROOT)

        elif "hkey_current_config" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CURRENT_CONFIG)

        elif "hkey_current_user" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_CURRENT_USER)

        elif "heky_users" in root_folder.lower():
            root_folder = ConnectRegistry(None, HKEY_USERS)
            

        try:
            registry_key = OpenKey(root_folder, key_path)

            system_value, reg_word = QueryValueEx(registry_key, sub_key)

            CloseKey(registry_key)
            
        except:
            # key not found 
            system_value = None


        return system_value


    def compare_registry_keys(self, registry_keys: list):
        
        for reg_key in registry_keys:

            root_folder = reg_key['root_folder']
            key_path = reg_key['key_path']
            sub_key = reg_key['sub_key']
            expected_value = reg_key['expected_value']
            description = reg_key['description']

            if expected_value == "None":
                
                if '!' in sub_key:
                    system_value = self.check_registry_key_exsists(
                            root_folder = root_folder,
                            key_path = key_path,
                            sub_key = sub_key
                    )

                    if system_value == None:
                        # means registry key doesn't exsists
                        CONFIG.SYSTEM_SCORE += 1
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1

                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is in compliance with standards",
                            "args" : []
                        }
                    else:
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1
                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is NOT in compliance with standards",
                            "args" : []
                        }
                        
                        CONFIG.WARNING_DICT["something"] = {
                            "Warning": "Registry Key Value not in compliance with the standards",
                            "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                            "System Value": system_value,
                            "Expected Value": None,
                            "Mitigation": """Change the registry key value to the standard expected value using regedit.exe after taking a backup of your current registry.
                                            Remove the key if expected_value = None or null""",
                            "Support Links": "https://www.dummies.com/computers/operating-systems/windows-xp-vista/how-to-modify-the-windows-registry/"
                        }

            else:
                system_value = self.get_registry_key_value(
                        root_folder = root_folder,
                        key_path = key_path,
                        sub_key = sub_key
                )

                if '!' in expected_value and 'r:' not in expected_value:

                    expected_value = int(expected_value.replace("!", ''))

                    if system_value != expected_value:
                        CONFIG.SYSTEM_SCORE += 1
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1

                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is in compliance with standards",
                            "args" : []
                        }

                    elif system_value == None:
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1
                        self.test_results['something'] = {
                            "result" :  "Registry Key not found",
                            "args" : []
                        }
                        CONFIG.WARNING_DICT["something"] = {
                            "Warning": "Registry Key not found",
                            "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                            "System Value": "Key doesn't exsist",
                            "Expected Value": expected_value,
                            "Mitigation": "Add the registry key to the system after taking a backup of your current registry.",
                            "Support Links": "https://support.microsoft.com/en-in/help/310516/how-to-add-modify-or-delete-registry-subkeys-and-values-by-using-a-reg"
                        }

                    else:
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1
                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is NOT in compliance with standards",
                            "args" : []
                        }
                        CONFIG.WARNING_DICT["something"] = {
                            "Warning": "Registry Key Value not in compliance with the standards",
                            "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                            "System Value": system_value,
                            "Expected Value": expected_value,
                            "Mitigation": "Change the registry key value to the standard expected value using regedit.exe after taking a backup of your current registry.",
                            "Support Links": "https://www.dummies.com/computers/operating-systems/windows-xp-vista/how-to-modify-the-windows-registry/"
                        }

                elif 'r:' in expected_value:
                    expected_value_regex = fr"{expected_value[expected_value.find(':')+1:]}"

                    match = self.util_obj.run_regex_search(expected_value_regex, system_value)

                    if '!r:' in expected_value:
                        if match is None:
                            CONFIG.SYSTEM_SCORE += 1
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1

                            self.test_results['something'] = {
                                "result" :  "Value of regsitry key is in compliance with standards",
                                "args" : []
                            }
                            
                        else:
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1
                            self.test_results['something'] = {
                                "result" :  "Value of regsitry key is NOT in compliance with standards",
                                "args" : []
                            }
                            CONFIG.WARNING_DICT["something"] = {
                                "Warning": "Registry Key Value not in compliance with the standards",
                                "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                                "System Value": system_value,
                                "Expected Value": expected_value,
                                "Mitigation": "Remove the key using regedit.exe after taking a backup of your current registry.",
                                "Support Links": "https://www.dummies.com/computers/operating-systems/windows-xp-vista/how-to-modify-the-windows-registry/"
                            }
                    else: 
                        if match is None:
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1
                            self.test_results['something'] = {
                                "result" :  "Value of regsitry key is NOT in compliance with standards",
                                "args" : []
                            }
                            CONFIG.WARNING_DICT["something"] = {
                                "Warning": "Registry Key Value not in compliance with the standards",
                                "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                                "System Value": system_value,
                                "Expected Value": expected_value,
                                "Mitigation": "Change the registry key value to the standard expected value (as per the regex) using regedit.exe after taking a backup of your current registry.",
                                "Support Links": "https://www.dummies.com/computers/operating-systems/windows-xp-vista/how-to-modify-the-windows-registry/"
                            }
                        else:
                            CONFIG.SYSTEM_SCORE += 1
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1

                            self.test_results['something'] = {
                                "result" :  "Value of regsitry key is in compliance with standards",
                                "args" : []
                            }

                else:
                    expected_value = int(expected_value)

                    if system_value == expected_value:
                        CONFIG.SYSTEM_SCORE += 1
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1

                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is in compliance with standards",
                            "args" : []
                        }
                        
                    else:
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1
                        self.test_results['something'] = {
                            "result" :  "Value of regsitry key is NOT in compliance with standards",
                            "args" : []
                        }
                        CONFIG.WARNING_DICT["something"] = {
                            "Warning": "Registry Key Value not in compliance with the standards",
                            "Registry Key": f"{root_folder}\\{key_path}\\{sub_key}",
                            "System Value": system_value,
                            "Expected Value": expected_value,
                            "Mitigation": "Change the registry key value to the standard expected value using regedit.exe after taking a backup of your current registry.",
                            "Support Links": "https://www.dummies.com/computers/operating-systems/windows-xp-vista/how-to-modify-the-windows-registry/"
                        }


    def get_registry_keys_from_database(self):
        registry_keys = []
        """
            Group1 : Root Folder
            Group2 : Key Path
            Group3 : Sub Key
            Group4 : Expected Value
            Group5 : Description
        """
        with open("db/win10_reg_key_db.txt", 'r') as read_object:
            matches = self.util_obj.run_regex_finditer(self.registry_key_regex, read_object.read())

            for match in matches:
                key_dict= {
                    "root_folder" : match.group(1),
                    "key_path" : match.group(2),
                    "sub_key" : match.group(3),
                    "expected_value" : match.group(4),
                    "description" : match.group(5),
                }
                registry_keys.append(key_dict)

        self.compare_registry_keys(registry_keys)


    def run_test(self):
        self.get_registry_keys_from_database()
        return self.test_results
