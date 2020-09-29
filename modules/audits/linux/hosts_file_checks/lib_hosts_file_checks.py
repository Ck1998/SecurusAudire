from modules.audits.base_model import BaseTest
import config as CONFIG


class HostsFileChecks(BaseTest):

    def __init__(self):
        super().__init__()
        self.test_results = {}
        self.hosts_file_location = f"{CONFIG.ROOT_DIR}etc/hosts"
        self.hosts_allow_file_location = f"{CONFIG.ROOT_DIR}etc/hosts.allow"
        self.hosts_file_checks_db = "db/linux_db/check_hosts_file_db.txt"
        self.db_regex = r"@(.+)(?:\s)!(.+)(?:\s)!(?:\s)?(.*)(?:\s)?"

    def check_hosts_file(self):
        try:
            with open(self.hosts_file_location, 'r') as read_obj:
                hosts_file_data = read_obj.read()
                with open(self.hosts_file_checks_db, 'r') as db_read_obj:
                    for checks in db_read_obj.readlines():
                        if "#" in checks[0] or len(checks) < 2:
                            continue

                        test_parameters = self.util_obj.run_regex_search(self.db_regex, checks)

                        file_name = test_parameters.group(1)
                        remote_host_name_to_check = test_parameters.group(2)
                        negative_message = test_parameters.group(3)

                        if file_name.lower() != "/etc/hosts":
                            continue

                        try:
                            isinstance(self.test_results[file_name], dict)
                        except KeyError:
                            self.test_results[file_name] = {}

                        regex_to_search = rf"(.*{remote_host_name_to_check})"

                        if self.util_obj.run_regex_search(regex=regex_to_search, data=hosts_file_data):
                            remote_host_name = remote_host_name_to_check.replace(r"\.", ".")
                            self.test_results[file_name][remote_host_name] = {
                                "Result": f"{negative_message} - {remote_host_name}"
                            }
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1

                            CONFIG.WARNING_DICT[
                                f"Irregularities found in file - {CONFIG.ROOT_DIR}{file_name} - {remote_host_name}"] = {
                                "Warning": negative_message,
                                "Support Link": "http://manpages.ubuntu.com/manpages/trusty/man5/hosts.5.html"
                            }
                        else:
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1
                            CONFIG.SYSTEM_SCORE += 1
                            remote_host_name = remote_host_name_to_check.replace(r"\.", ".")
                            self.test_results[file_name][remote_host_name] = {
                                "Result": f"Not found in {file_name}"
                            }

        except FileNotFoundError:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1
            CONFIG.WARNING_DICT[f'{CONFIG.ROOT_DIR}etc/hosts not found'] = {
                "Warning": f'{CONFIG.ROOT_DIR}etc/hosts not found on the system',
                "Support Link": "http://manpages.ubuntu.com/manpages/trusty/man5/hosts.5.html"
            }

    def check_hosts_allow_file(self):
        try:
            with open(self.hosts_allow_file_location, 'r') as read_obj:
                hosts_file_data = read_obj.read()
                with open(self.hosts_file_checks_db, 'r') as db_read_obj:
                    for checks in db_read_obj.readlines():
                        if "#" in checks[0] or len(checks) < 2:
                            continue

                        test_parameters = self.util_obj.run_regex_search(self.db_regex, checks)
                        file_name = test_parameters.group(1)
                        remote_host_name_to_check = test_parameters.group(2)
                        negative_message = test_parameters.group(3)

                        if file_name.lower() != "/etc/hosts.allow":
                            continue

                        try:
                            isinstance(self.test_results[file_name], dict)
                        except KeyError:
                            self.test_results[file_name] = {}

                        regex_to_search = rf"(.*{remote_host_name_to_check})"

                        if self.util_obj.run_regex_search(regex=regex_to_search, data=hosts_file_data):
                            remote_host_name = remote_host_name_to_check.replace(r"\.", ".")
                            self.test_results[file_name][remote_host_name_to_check] = {
                                "Result": f"{negative_message} - {remote_host_name}"
                            }
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1

                            CONFIG.WARNING_DICT[
                                f"Irregularities found in file - {CONFIG.ROOT_DIR}{file_name} - {remote_host_name}"] = {
                                "Warning": negative_message,
                                "Support Link": "https://linux.die.net/man/5/hosts.allow"
                            }
                        else:
                            CONFIG.TOTAL_SCORE_POSSIBLE += 1
                            CONFIG.SYSTEM_SCORE += 1
                            remote_host_name = remote_host_name_to_check.replace(r"\.", ".")
                            self.test_results[file_name][remote_host_name] = {
                                "Result": f"Not found in {file_name}"
                            }

        except FileNotFoundError:
            CONFIG.TOTAL_SCORE_POSSIBLE += 1

    def run_test(self):
        self.check_hosts_file()
        self.check_hosts_allow_file()
        return self.test_results

# TODO: Use better method for this audit
