# utils classes
from modules.utils.lib_general_utils import Utils

# report generation classes
from modules.report_generation.json_report.generate_json_report import GenerateJsonReport
from modules.report_generation.web_report.generate_web_report import GenerateWebReport


class ReportGenController:
    
    def __init__(self, full_report: dict, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.full_report = full_report
        util_obj = Utils()
        self.timestamp = util_obj.get_current_datetime().strftime("%d-%m-%Y %H_%M_%S")
        self.timestamp = f"Date - {self.timestamp.split(' ')[0]}, Time - {self.timestamp.split(' ')[1]}"

    def generate_json_report(self):
        json_report_obj = GenerateJsonReport(self.full_report, self.save_folder_location, self.timestamp)

        json_report_obj.generate_report()

    def generate_web_report(self):
        web_report_obj = GenerateWebReport(self.full_report, self.save_folder_location, self.timestamp)

        web_report_obj.generate_report()

    def controller(self):
        self.generate_json_report()
        self.generate_web_report()