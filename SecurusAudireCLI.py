from modules.audit_controller import AuditController


class SecurusAudireCLI:

    def __init__(self):
        super().__init__()
        self.save_folder_location = ""

    def run_audit(self):
        audit_controller_object = AuditController(self.save_folder_location)
        audit_status = audit_controller_object.controller()
        if audit_status == 0:
            print('System Audit Complete. You can view generated reports at - '+self.save_folder_location+"/SecurusAudire_Reports/")
        else:
            answer = input('SecurusAudire encountered some errors, are you running the script as root?') 
            if 'n' in answer.lower():
                print('Script should be executed with root privileges!!!')
            else:
                print('Please exit and try again!!!')

    def run_cli(self):
        self.save_folder_location = input("Enter location to save generated reports (default: /var/log/SecurusAudire_Reports)- ")

        if len(self.save_folder_location) == 0:
            self.save_folder_location = "/var/log"

        self.run_audit()


if __name__ == "__main__":
    cli_obj = SecurusAudireCLI()
    cli_obj.run_cli()