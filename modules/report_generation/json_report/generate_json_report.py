from modules.report_generation.report_generator_base import ReportGenBase

class GenerateJsonReport(ReportGenBase):

    def __init__(self, audit_result: dict, save_folder_location: str, timestamp):
        super().__init__()
        self.audit_result = audit_result
        self.save_folder_location = save_folder_location
        self.timestamp = timestamp


    def parse_result(self):
        file_content = self.util_obj.convert_dict_to_json(self.audit_result)

        self.create_file(file_content)

    def create_file(self, file_content):
        
        if not self.util_obj.check_file_exsists(self.save_folder_location+"/SecurusAudire_Reports"):
            res = self.util_obj.get_command_output(['mkdir', self.save_folder_location+'/SecurusAudire_Reports'])

        with open(self.save_folder_location+"/SecurusAudire_Reports/json_report-"+str(self.timestamp)+".json", 'w+') as write_file_obj:
            write_file_obj.write(file_content)
    
    def generate_report(self):
        self.parse_result()