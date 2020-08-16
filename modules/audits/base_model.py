from modules.utils.lib_general_utils import Utils
from config import ROOT_DIR


class BaseTest(object):

    __disabled__ = False
    subclasses = []

    def __init__(self):
        self.util_obj = Utils()
        self.ROOT_DIR = ROOT_DIR

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @staticmethod
    def remove_duplicates_from_list(arr: list):
        return list(dict.fromkeys(arr))

    def run_test(self):
        return None
