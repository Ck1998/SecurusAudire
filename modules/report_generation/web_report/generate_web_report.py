from modules.report_generation.report_generator_base import ReportGenBase

class GenerateWebReport(ReportGenBase):

    def __init__(self, audit_result: dict, save_folder_location: str, timestamp):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_resul = audit_result
        self.timestamp = timestamp

    def parse_result(self):
        self.file_content = "HIIII"

    def create_file(self):
        
        if not self.util_obj.check_file_exsists(self.save_folder_location+"/SecurusAudire_Reports"):
            res = self.util_obj.get_command_output(['mkdir', self.save_folder_location+'/SecurusAudire_Reports'])

        with open(self.save_folder_location+"/SecurusAudire_Reports/web_report-"+str(self.timestamp)+".html", 'w+') as write_file_obj:
            write_file_obj.write(self.file_content)
    
    def generate_report(self):
        
        self.parse_result()
        self.create_file()
