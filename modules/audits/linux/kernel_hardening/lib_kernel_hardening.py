from modules.audits.base_model import BaseTest
import config as CONFIG


class KernelHardeningAudits(BaseTest):
    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.sysctl_keys_regex = r"(.+)(?:[\s])=(?:[\s])(.+)"
        self.parse_db_regex = r"(.+)(?:[\s])@(?:[\s])(.*)(?:[\s])!(?:[\s])(.*)(?:[\s]):(?:[\s])(.*)(?:[\s]):(?:[\s])url:(.*)"
        self.db_location = "db/linux_db/kernel_hardening_db.txt"
        self.test_result = {}

    def format_sysctl_keys(self, raw_keys: str):
        matches = self.util_obj.run_regex_finditer(self.sysctl_keys_regex, raw_keys)

        formatted_keys = {}

        for match in matches:
            formatted_keys[match.group(1)] = match.group(2)

        return formatted_keys

    def get_all_sysctl_keys(self):
        sysctl_keys_raw = self.util_obj.get_command_output(['sysctl', '-a'])

        sysctl_keys_formatted = self.format_sysctl_keys(sysctl_keys_raw)

        return sysctl_keys_formatted

    def check_sysctl_keys(self, db_dict: dict):

        # get system sysctl keys
        system_sysctl_keys = self.get_all_sysctl_keys()

        # checking against databse
        for sysctl_key in db_dict.keys():
            expected_value = db_dict[sysctl_key]['expected_value']

            try:

                system_key_value = system_sysctl_keys[sysctl_key]

            except:

                continue

            expected_value = expected_value.replace(",", " ").split()
            system_key_value = system_key_value.split()

            # flag variable is used to check if the system_key_value is equal to the expected value
            # flag = False: that means no discrepency is present
            # flag = True: that means discrepency is present

            flag = False

            for key in system_key_value:
                if key not in expected_value:
                    flag = True
                    break

            if not flag:
                CONFIG.SYSTEM_SCORE += 1
                CONFIG.TOTAL_SCORE_POSSIBLE += 1
                self.test_result[sysctl_key] = {}
                self.test_result[sysctl_key].update(result="Sysctl key value in compliance with standards", args={
                    "description": db_dict[sysctl_key]['description'],
                    "Support Link": db_dict[sysctl_key]['support_link']
                })
            else:
                CONFIG.TOTAL_SCORE_POSSIBLE += 1
                CONFIG.WARNING_DICT[sysctl_key] = {
                    "Warning": f"{sysctl_key} key value not in complaince with standards",
                    "Value Found in System": system_key_value,
                    "Expected Value": expected_value,
                    "description": db_dict[sysctl_key]['description'],
                    "Support Link": db_dict[sysctl_key]['support_link']
                }
                self.test_result[sysctl_key] = {}
                self.test_result[sysctl_key].update(result="Sysctl key value not in compliance with standards", args={
                    "Value Found in System": system_key_value,
                    "Expected Value": expected_value,
                })

    def parse_db(self):
        db_dict = {}
        with open(self.db_location, 'r') as db_read_obj:
            matches = self.util_obj.run_regex_finditer(self.parse_db_regex, db_read_obj.read())

            # keys to extract from the database
            # match.group(1) : sysctl (No use as of this now, just meant for reference purpose)
            # match.group(2) : sysctl key to check
            # match.group(3) : Expected value of that sysctl key 
            # match.group(4) : Decription of the sysctl key (if any)
            # match.group(5) : reference links (if any)
            #
            # This <for_loop> below will generate the following dictionary
            # {
            #   <sysctl_key_1>: {
            #       <expected_value>:"",
            #       <description>:"",
            #       <support_link>:""
            #   },
            #   <sysctl_key_2>: {
            #       <expected_value>:"",
            #       <description>:"",
            #       <support_link>:""
            #   } 
            #   ..... and so on
            # }

            for match in matches:
                db_dict[match.group(2)] = {}
                db_dict[match.group(2)].update(expected_value=match.group(3), description=match.group(4),
                                               support_link=match.group(5))

        self.check_sysctl_keys(db_dict)

    def run_test(self):
        self.parse_db()
        return self.test_result
