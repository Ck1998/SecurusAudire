from modules.utils.lib_general_utils import Utils
from config import ROOT_DIR


class BaseTest(object):
    def __init__(self):
        super().__init__()
        self.util_obj = Utils()
        self.ROOT_DIR = ROOT_DIR

    def run_test(self):
        return None