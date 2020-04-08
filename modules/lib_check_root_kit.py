import os
import json
import glob

class CheckRootKits:
    def __init__(self):
        super().__init__()
        self.database_file = "db/check_root_kit_db.txt"
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

    def check_file_exsists(self, file_path):
        result = os.path.exists(self.ROOT_DIR+file_path)
        if result:
            return {
                        "result": "infected",
                        "args": None
                    }
        else:
            return {
                        "result": "not found",
                        "args": None
                    }

    def glob_check(self,file_path,file_name):
        files = glob.iglob(file_path+'**/'+file_name, recursive = True) 
        if files is None:
            result = {}
            for filename in files:
                result[file_name] = {
                        "result": "infected",
                        "args": None
                    }
            return result

        else:
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

                        result = self.glob_check(file_path, file_name)
                        self.test_result[__module__][__file__] = result

                    else: 
                        result = self.check_file_exsists(__file__)
                        self.test_result[__module__][__file__] = result

    def run_test(self):
        self.parse_db_file()
        return self.test_result