import os
import sys

LOG_FILE = "SecurusAudire_AuditResult"

PATH_VARIABLE = os.environ["PATH"].split(":")

# os.path.abspath(sys.executable)[0] will be None in case of POISX Systems
ROOT_DIR = '/' if os.path.abspath(sys.executable)[0] is None else os.path.abspath(sys.executable)[0]


