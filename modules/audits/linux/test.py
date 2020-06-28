from modules.audits.base_model import BaseTest


def get_tool_class() -> BaseTest:
    integrations = BaseTest.__subclasses__()
    for cls in integrations:
        print(cls.__name__)

get_tool_class()