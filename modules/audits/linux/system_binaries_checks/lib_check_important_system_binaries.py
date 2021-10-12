from modules.audits.base_model import BaseTest
import config as CONFIG


class ImportantSystemBinariesCheck(BaseTest):

    def __init__(self):
        super().__init__()
        self.test_results = {}
        self.database_location = "db/linux_db/linux_system_binaries_check_audits_db.txt"
        self.record_regex = r'([sr])(?:\s)@(?:\s)?(.*)(?:\s):(?:\s)?(.*)(?:\s)>(?:\s)?(.*)(?:\s)!(?:\s)?(.*)(?:\s):(?:\s)?(.*)(?:\s)'

    def parse_database_file(self):
        with open(self.database_location, 'r') as read_obj:
            for line in read_obj.readlines():
                if '#' in line[0] or len(line) < 2:
                    continue

                test_parameters = self.util_obj.run_regex_search(regex=self.record_regex , data=line)

                search_type = test_parameters.group(1)
                test_name = test_parameters.group(2)
                binary_name = test_parameters.group(3)
                search_directories = test_parameters.group(4)
                positive_message = test_parameters.group(5)
                negative_message = test_parameters.group(6)

                if search_type.lower() == 's':
                    found_flag = False
                    for search_directory in search_directories.split(" "):
                        if self.util_obj.check_file_exists(f"{CONFIG.ROOT_DIR}{search_directory}{binary_name}"):
                            found_flag = True
                            break

                    if not found_flag:
                        self.test_results[binary_name] = {
                            "Result": negative_message
                        }
                        CONFIG.SUGGESTIONS_DICT[binary_name] = {
                            "Suggestion": f"{binary_name} is an important system binary, install it for additional "
                                          f"system protextion ",
                            "Support Link": "NA"
                        }
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1
                    else:
                        self.test_results[binary_name] = {
                            "Result": positive_message
                        }
                        CONFIG.SYSTEM_SCORE += 1
                        CONFIG.TOTAL_SCORE_POSSIBLE += 1

    def run_test(self):
        self.parse_database_file()
        return self.test_results
