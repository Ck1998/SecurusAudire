from modules.audits.base_model import BaseTest
import os


class FilePermissionAudits(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_result = {}

    def get_file_permissons(self, filepath):
        return None

    def run_test(self):
        return None