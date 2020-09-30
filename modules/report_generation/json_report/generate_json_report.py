from modules.report_generation.report_generator_base import ReportGenBase
from config import CURR_SYSTEM_PLATFORM

from os import makedirs


class GenerateJsonReport(ReportGenBase):

    def __init__(self, full_report: dict, save_folder_location: str, timestamp):
        super().__init__()
        self.full_report = full_report
        self.save_folder_location = save_folder_location
        self.timestamp = timestamp

    def create_file(self, file_content):

        if CURR_SYSTEM_PLATFORM == "windows":
            if not self.util_obj.check_file_exsists(self.save_folder_location + r"\SecurusAudire_Reports"):
                makedirs(self.save_folder_location + r'\SecurusAudire_Reports')

            complete_location = rf"{self.save_folder_location}\SecurusAudire_Reports\json_report-{self.timestamp}.json"

        else:
            if not self.util_obj.check_file_exsists(self.save_folder_location + r"/SecurusAudire_Reports"):
                makedirs(self.save_folder_location + r'/SecurusAudire_Reports')

            complete_location = f"{self.save_folder_location}/SecurusAudire_Reports/" \
                                f"json_report-{str(self.timestamp)}.json"

        with open(complete_location, 'w+') as write_file_obj:
            write_file_obj.write(file_content)

    def parse_result(self):
        system_score = self.full_report["System Score"]
        total_score_possible = self.full_report["Total Score Possible"]

        try:
            hardening_index = round((system_score / total_score_possible) * 100, 2)
        except ZeroDivisionError:
            hardening_index = 0.00
        self.full_report['Hardening Index'] = f"{hardening_index} %"
        self.full_report['System Detected'] = CURR_SYSTEM_PLATFORM

        file_content = self.util_obj.convert_dict_to_json(self.full_report)

        self.create_file(file_content)

    def generate_report(self):
        self.parse_result()
