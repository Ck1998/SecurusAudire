# utils classes
from modules.utils.lib_general_utils import Utils

# report generation classes
from modules.report_generation.json_report.generate_json_report import GenerateJsonReport
from modules.report_generation.web_report.generate_web_report import GenerateWebReport


class ReportGenController:
    
    def __init__(self, audit_result: dict, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.audit_result = audit_result
        util_obj = Utils()
        self.timestamp = util_obj.get_current_datetime()

    def generate_json_report(self):
        json_report_obj = GenerateJsonReport(self.audit_result, self.save_folder_location, self.timestamp)

        json_report_obj.generate_report()

    def generate_web_report(self):
        web_report_obj = GenerateWebReport(self.audit_result, self.save_folder_location, self.timestamp)

        web_report_obj.generate_report()

    def controller(self):
        self.generate_json_report()
        self.generate_web_report()