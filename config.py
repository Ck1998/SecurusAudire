import os
import sys

PATH_VARIABLE = os.environ["PATH"].split(":")

# os.path.abspath(sys.executable)[0] will be None in case of POISX Systems
ROOT_DIR = '/' if os.path.abspath(sys.executable)[0] is None else os.path.abspath(sys.executable)[0]

# scoring variables
SYSTEM_SCORE = 0
TOTAL_SCORE_POSSIBLE = 0

# Supporting DICTIONARIES
SUGGESTIONS_DICT = {}
WARNING_DICT = {}