from modules.report_generation.report_generator_base import ReportGenBase

class GenerateJsonReport(ReportGenBase):

    def __init__(self, full_report: dict, save_folder_location: str, timestamp):
        super().__init__()
        self.full_report = full_report
        self.save_folder_location = save_folder_location
        self.timestamp = timestamp


    def parse_result(self):
        file_content = self.util_obj.convert_dict_to_json(self.full_report)

        self.create_file(file_content)

    def create_file(self, file_content):
        
        if not self.util_obj.check_file_exsists(self.save_folder_location+"/SecurusAudire_Reports"):
            res = self.util_obj.get_command_output(['mkdir', self.save_folder_location+'/SecurusAudire_Reports'])

        self.save_folder_location = self.save_folder_location.replace("\\", '/')
        with open(self.save_folder_location+"/SecurusAudire_Reports/json_report-"+str(self.timestamp)+".json", 'w+') as write_file_obj:
            write_file_obj.write(file_content)
    
    def generate_report(self):
        self.parse_result()