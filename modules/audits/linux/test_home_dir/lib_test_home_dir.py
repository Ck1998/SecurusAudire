from modules.audits.base_model import BaseTest
import re
import config as CONFIG


class TestHomeDir(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.home_dir_regex = r".*:.*:.*:.*:.*:(.*):.*[\s]"
        self.home_dir_location = self.ROOT_DIR + "etc/passwd"
        self.ignore_dir_list = []
        self.test_result = {}

    def get_shell_history_files(self, dir_name):
        return self.util_obj.recursive_search(dir_name, ".*history")

    def check_for_suspicious_shell_history_files(self, home_dir_list: list):
        susp_file_list = []
        self.test_result['Checking For Suspicious Shell History Files'] = {}

        while '/' in home_dir_list:
            home_dir_list.remove('/')

        for dir_name in home_dir_list:
            shell_history_files_list = self.get_shell_history_files(dir_name)
            for shell_history_file in shell_history_files_list:

                result = self.util_obj.check_is_file(shell_history_file)
                if not result:
                    susp_file_list.append(shell_history_file)

        if len(susp_file_list) == 0:
            CONFIG.SYSTEM_SCORE += 1
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            self.test_result['Checking For Suspicious Shell History Files'].update(
                result="No suspicious shell history files found", args=None)
        else:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.WARNING_DICT["Suspicious Shell History Files"] = {
                "Warning": "Suspicious Shell History files found",
                "Suspicious Shell history files": susp_file_list
            }
            self.test_result['Checking For Suspicious Shell History Files'].update(
                result="Suspicious shell history files found", args=susp_file_list)

    def test_home_dir(self):
        home_dir_list = []

        self.test_result['Checking For Home Directories'] = {}
        with open(self.home_dir_location, 'r') as file_read_obj:
            matches = re.finditer(self.home_dir_regex, file_read_obj.read())
            if matches is None:
                self.test_result['Checking For Home Directories'].update(result="No Home directries found")
            else:
                for match in matches:
                    home_dir_list.append(match.group(1))

                home_dir_list = self.remove_duplicates_from_list(home_dir_list)

                self.test_result['Checking For Home Directories'].update(result="Home directories found",
                                                                         args=home_dir_list)
                self.check_for_suspicious_shell_history_files(home_dir_list)

    def run_test(self):
        self.test_home_dir()
        return self.test_result
