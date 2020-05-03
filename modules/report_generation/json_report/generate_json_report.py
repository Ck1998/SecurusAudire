from modules.report_generation.report_generator_base import ReportGenBase

from os import makedirs

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
        
        if not self.util_obj.check_file_exsists(self.save_folder_location+r"\SecurusAudire_Reports"):
            makedirs(self.save_folder_location+r'\SecurusAudire_Reports')

        complete_location = rf"{self.save_folder_location}\SecurusAudire_Reports\json_report-"+str(self.timestamp)[:str(self.timestamp).find(' ')]+".json"
    
        with open(complete_location, 'w') as write_file_obj:
            write_file_obj.write(file_content)

    def generate_report(self):
        self.parse_result()