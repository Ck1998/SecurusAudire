from modules.base_model import BaseTest
import subprocess

class CheckAuthenticationModule(BaseTest):

    def __init__(self):
        super().__init__()
        self.test_result = {}
        self.passwd_file_location = self.ROOT_DIR+"etc/passwd"
        self.all_user_regex = r"(.*):(.*):(.*):(.*):(.*):(.*):(.*)"
        self.all_user_details = {}
        self.is_all_user_details_fetched = False

    def get_keys(self, arr: dict, val):
        
        key_arr = []
        
        for key, value in arr.items():
            if val == value:
                key_arr.append(key)

        return key_arr

    def get_user_details_from_file(self, regex: str=None, get_all_details: bool=False):
        with open(self.passwd_file_location, 'r') as file_read_obj:

            if get_all_details:
                matches = self.util_obj.run_regex_finditer(self.all_user_regex, file_read_obj.read())
                for match in matches:
                    self.all_user_details[match.group(1)] = {}
                    self.all_user_details[match.group(1)].update(
                        Encrypted_Password = match.group(2),
                        UID = match.group(3),
                        GID = match.group(4),
                        GECOS = match.group(5),
                        home_dir = match.group(6),
                        login_shell = match.group(7)
                    )
                
                return None

            else:
                matches = self.util_obj.run_regex_finditer(self.all_user_regex, file_read_obj.read())
                return matches

    def check_users_with_uid_0(self):
        user_with_uid_0_regex = r"(.*):.*:0:[\d]+:.*"

        test_result = {}
        users = []

        matches = self.get_user_details_from_file(user_with_uid_0_regex)

        for match in matches:
            users.append(match.group(1))

        if len(users)>1:
            test_result.update(result = "Found more than one administrator accounts", args = {"Users with UID 0 in etc/passwd": users})
        elif len(users)==1:
            test_result.update(result = "Found one administrator account", args = {"User with UID 0 in etc/passwd": users})
        else:
            test_result.update(result = "No administrator account found in etc/passwd", args = None)

        return test_result

    def check_non_unique_accounts(self):

        test_result = {}

        if self.is_all_user_details_fetched == False:
            self.is_all_user_details_fetched == True
            matches = self.get_user_details_from_file(get_all_details=True)

        uid_dict = {}
        uid_num_array = []

        # generate UID array
        for key in self.all_user_details.keys():
            uid_dict[key] = self.all_user_details[key].get("UID")
            uid_num_array.append(self.all_user_details[key].get("UID"))

        temp_duplicates_array = [i for i in uid_num_array if uid_num_array.count(i) > 1]

        duplicates_array = {}
        for val in temp_duplicates_array:
            duplicates = self.get_keys(uid_dict, val)
            duplicates_array[val] = (duplicates)
        
        if len(duplicates_array) == 0:
            test_result = {
                "result": "All accounts found in etc/passwd file are unique"
            }
        else:
            test_result = {
                "result": "All accounts found in etc/passwd file are not unique, follwoing accounts have same UID number",
                "args" : duplicates_array
            }

        return test_result

    def check_group_file_with_chkgrp(self):
        chkgrp_file_location = self.ROOT_DIR+"usr/sbin/chkgrp"

        if self.util_obj.check_file_exsists(chkgrp_file_location):
            # chkgrp binary present performing additional audits
            command_output = self.util_obj.get_command_output([self.ROOT_DIR+"usr/sbin/chkgrp"])

            if 'is fine' in command_output:
                test_result = {
                    "result": "chkgrp test performed, Group file seems to be ok.",
                    "args" : None
                }
            else:
                test_result = {
                    "result": "chkgrp found some errors. Run the tool manually to see details.",
                    "args" : command_output
                }
        else:
            # chkgrp binary not present skipping additional audits
            test_result = {
                "result": "chkgrp binary not found, skipping additional tests",
                "args" : None
            }
            
        return test_result

    def check_group_file_with_grpck(self):
        grpck_file_location = self.ROOT_DIR+"usr/sbin/grpck"

        if self.util_obj.check_file_exsists(grpck_file_location):
            # grpck binary present performing additional audits
            command_output = self.util_obj.get_command_output([self.ROOT_DIR+"usr/sbin/grpck", '-r'])

            if len(command_output) == 0:
                test_result = {
                    "result": "grpck binary didn't find any errors in the group files",
                    "args" : None
                }
            else:
                test_result = {
                    "result": "grpck binary found errors in one or more group files",
                    "args" : command_output
                }
        else:
            # grpck binary not present skipping additional audits
            test_result = {
                "result": "grpck binary not found, skipping additional tests",
                "args" : None
            }
            
        return test_result

    def check_unique_group_ids(self):
        
        test_result = {}

        if self.is_all_user_details_fetched == False:
            self.is_all_user_details_fetched == True
            matches = self.get_user_details_from_file(get_all_details=True)

        gid_dict = {}
        gid_num_array = []
        temp_duplicates_array = []

        # generate gid array
        for key in self.all_user_details.keys():
            gid_dict[key] = self.all_user_details[key].get("GID")
            gid_num_array.append(self.all_user_details[key].get("GID"))

        temp_duplicates_array = [i for i in gid_num_array if gid_num_array.count(i) > 1]

        duplicates_array = {}
        for val in temp_duplicates_array:
            duplicates = self.get_keys(gid_dict, val)
            duplicates_array[val] = duplicates
        
        if len(duplicates_array) == 0:
            test_result = {
                "result": "All accounts found in etc/passwd file are unique"
            }
        else:
            test_result = {
                "result": "All accounts found in etc/passwd file are not unique, follwoing accounts have same GID number",
                "args" : duplicates_array
            }

        return test_result

    def check_unique_group_names(self):
        test_result = {}
        group_name_regex = r"(.*):.*:.*:.*"
        group_file_location = self.ROOT_DIR+"etc/group"

        group_name_array = []
        unique_group_name_array = []
        not_unique_group_name_array = []

        with open(group_file_location, 'r') as file_read_obj:
            matches = self.util_obj.run_regex_finditer(group_name_regex, file_read_obj.read())

        for match in matches:
            group_name_array.append(match.group(1))
            if match.group(1) not in unique_group_name_array:
                unique_group_name_array.append(match.group(1))
            else:
                not_unique_group_name_array.append(match.group(1))
        
        if len(not_unique_group_name_array) == 0:
            test_result = {
                "result": "All group names are unique",
                "args" : None
            }
        else:
            test_result = {
                "result": "All group names are not unique",
                "args" : not_unique_group_name_array
            }

        return test_result

    def check_passwd_file_consistency(self):
        pwck_file_location = self.ROOT_DIR+"usr/sbin/pwck"

        if self.util_obj.check_file_exsists(pwck_file_location):
            # pwck binary present performing additional audits
            try:
                command_output = subprocess.check_output([self.ROOT_DIR+"usr/sbin/pwck", '-r'])
            except subprocess.CalledProcessError as e:
                
                test_result = {
                    "result": "pwck check found one or more errors/warnings in the password file",
                    "args" : None
                }

                return test_result
            
            test_result = {
                "result": "pwck check didn't find any errors in the password file.",
                "args" : None
            }

        else:
            # pwck binary not present skipping additional audits
            test_result = {
                "result": "pwck binary not found, skipping additional tests",
                "args" : None
            }
            
        return test_result

    def query_user_accounts(self):
        test_result = {}

        if self.is_all_user_details_fetched == False:
            self.is_all_user_details_fetched == True
            matches = self.get_user_details_from_file(get_all_details=True)

        # get min uid from /etc/login.def
        min_uid_regex = r"^UID_MIN[\s]*([\d]+)"
        with open(self.ROOT_DIR+"etc/login.defs") as file_read_obj:
            match = self.util_obj.run_regex_search(min_uid_regex, file_read_obj.read())

            if match is not None:
                min_uid = int(match.group(1))
            else:
                min_uid = 1000   # standard value
        
        users = []

        for account_name in self.all_user_details.keys():
            UID = int(self.all_user_details[account_name].get("UID"))
            if UID == 0 or UID > min_uid:
                temp = {}
                temp[account_name] = UID
                users.append(temp)

        if len(users) == 0:
            test_result = {
                "result": "No users found/unknown result",
                "args" : None
            }
        else:
            test_result = {
                "result": "List of system users (non daemons)",
                "args" : users
            }

        return test_result

    def query_nis_plus_auth_support(self):
        nis_file_location = self.ROOT_DIR+"etc/nsswitch.conf"

        if self.util_obj.check_file_exsists(nis_file_location):
            
            nis_regex = r"(^passwd):[\s]+(.+)"
            with open(nis_file_location, 'r') as file_read_obj:
                match = self.util_obj.run_regex_search(nis_regex, file_read_obj.read())
            
                if match:
                    if "compat" in match.group(1) or "nisplus" in match.group(1):
                        test_result = {
                            "result": "NIS+ authentication enabled",
                            "args" : None
                        }
                    else:
                        test_result = {
                            "result": "NIS+ authentication not enabled",
                            "args" : None
                        }
                else:
                    test_result = {
                        "result": "NIS+ authentication not enabled",
                        "args" : None
                    }
        else:

            test_result = {
                "result": "/etc/nsswitch.conf not found",
                "args" : None
            }
            
        return test_result

    def query_nis_auth_support(self):
        nis_file_location = self.ROOT_DIR+"etc/nsswitch.conf"

        if self.util_obj.check_file_exsists(nis_file_location):
            
            nis_regex = r"(^passwd):[\s]+(.+)"
            with open(nis_file_location, 'r') as file_read_obj:
                match = self.util_obj.run_regex_search(nis_regex, file_read_obj.read())
            
            if match:
                if "compat" in match.group(1) or "nis" in match.group(1):
                    test_result = {
                        "result": "NIS authentication enabled",
                        "args" : None
                    }
                else:
                    test_result = {
                        "result": "NIS authentication not enabled",
                        "args" : None
                    }
            else:
                test_result = {
                    "result": "NIS authentication not enabled",
                    "args" : None
                }
        else:

            test_result = {
                "result": "/etc/nsswitch.conf not found",
                "args" : None
            }
            
        return test_result

    def check_sudoers_file(self):
        test_result= {}
        sudoers_file_location = ["etc/sudoers","usr/local/etc/sudoers","usr/pkg/etc/sudoers"]
        sudoers_file_array = []

        for sudoer_file in sudoers_file_location:
            if self.util_obj.check_file_exsists(self.ROOT_DIR+sudoer_file):
                sudoers_file_array.append(sudoer_file)

        if len(sudoers_file_array) == 0:
            test_result = {
                "result": "NO sudoers file(s) found",
                "args" : None
            }
        else:
            test_result = {
                "result": "Sudoers file(s) found",
                "args" : sudoers_file_array
            }

        return test_result

    def run_all_functions(self):
        self.test_result = {
            "Users with UID 0": self.check_users_with_uid_0(),
            "Non unique accounts": self.check_non_unique_accounts(),
            "Checking group file using chkgrp":self.check_group_file_with_chkgrp(),
            "Checking group file using grpck":self.check_group_file_with_grpck(),
            "Non unique group ids":self.check_unique_group_ids(),
            "Non unique group name":self.check_unique_group_names(),
            "Password file consistency":self.check_passwd_file_consistency(),
            "User Accounts":self.query_user_accounts(),
            "NIS+ Authentication Support":self.query_nis_plus_auth_support(),
            "NIS Authentication Support":self.query_nis_auth_support(),
            "Checking sudoers file":self.check_sudoers_file()
        }
    
    def run_test(self):
        self.run_all_functions()
        return self.test_result