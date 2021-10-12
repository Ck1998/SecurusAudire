from modules.utils.lib_general_utils import Utils


class ReportGenBase(object):

    def __init__(self):
        super().__init__()
        self.util_obj = Utils()

    def parse_result(self):
        return "Custom Function Not Implemented"

    def create_file(self, file_content):
        return "Custom Function Not Implemented"

    def generate_report(self):
        return "Custom Function Not Implemented"
