from modules.audits.base_model import BaseTest
import config as CONFIG

# TODO: Refractor this file

import os
import glob

class CheckRootKits(BaseTest):
    def __init__(self):
        super().__init__()
        self.database_file = "db/linux_db/check_root_kit_db.txt"
        self.check_root_kit = {}
        self.ROOT_DIR = "/"
        self.test_result = {}

    """

        rootkit = {
            "module_name": {
                "file_name": {
                    "result": "",
                    "args": ""
                },
                "file_name": {
                    "result": "",
                    "args": ""
                },
            }
        }

    """

    def check_file_exsists(self, file_path, module):
        result = os.path.exists(self.ROOT_DIR+file_path)
        if result:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.WARNING_DICT[module] = {
                    "Warning": f"Possible {module} infection",
                    "Infected Files": f"{file_path}",
                    "Mitigation": "Remove the infected files using a live CD OS",
                    "Support Links": None
            }
            return {
                        "result": "possible infection detected",
                        "args": None
                    }
        else:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.SYSTEM_SCORE += 1
            return {
                        "result": "not found",
                        "args": None
                    }

    def glob_check(self,file_path,file_name, module):
        files = glob.iglob(file_path+'**/'+file_name, recursive = True) 
        if files is None:
            result = {}
            for filename in files:
                CONFIG.TOTAL_SCORE_POSSIBLE += 1
                CONFIG.WARNING_DICT[module] = {
                    "Warning": f"Possible {module} infection",
                    "Infected Files": filename,
                    "Mitigation": "Remove the infected files using a live CD OS",
                    "Support Links": None
                }
                result[file_name] = {
                        "result": "infected",
                        "args": None
                    }
            return result

        else:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.SYSTEM_SCORE += 1
            return {
                        "result": "not found",
                        "args": None
                    }

    #   272 checks
    #   60 rootkits

    def parse_db_file(self):
        with open(self.database_file, "r") as dbread:
            for line in dbread:
                if '#' not in line[0] and len(line) != 1 and len(line) != 0:
                    line = line.strip()
                    __module__ = line[line.find('@')+1:line.find('!')-1]
                    
                    if __module__ not in self.test_result.keys():
                        self.test_result[__module__] = {}

                    __file__ = line[line.find('!')+1:]
                    if '*' in __file__:
                        file_path = __file__[:__file__.find('*')]
                        file_name = __file__[__file__.find('/')+1:]
                        if len(file_path) == 0:
                            # remove this in production
                            file_path = '/usr/bin'

                        result = self.glob_check(file_path, file_name, __module__)
                        self.test_result[__module__][__file__] = result

                    else: 
                        result = self.check_file_exsists(__file__, __module__)
                        self.test_result[__module__][__file__] = result

    def run_test(self):
        self.parse_db_file()
        return self.test_result
