from utils.lib_general_utils import Utils

class BaseTest(object):
    def __init__(self):
        super().__init__()
        self.util_obj = Utils

    def run_test(self):
        return None