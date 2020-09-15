from modules.audits.base_model import BaseTest


class CustomTestExample(BaseTest):

    __disabled__ = False

    def __init__(self):
        # dictionary to store results
        super().__init__()
        self.test_results = {}

    def simulate_custom_audits(self):
        self.test_results['This is a custom audit example'] = {
            "Result": "Pass",
            "Args": "This is an example of a custom audit"
        }

    def run_test(self):
        # User should define custom tests here
        # User can create separate functions and call each function in this function
        # function run_test is to be overridden in the child class
        # this function acts as a driver for this custom test
        self.simulate_custom_audits()

        # return the dictionary created to the calling function
        return self.test_results
