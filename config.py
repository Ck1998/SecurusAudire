import os
import sys
from platform import system


PATH_VARIABLE = os.environ["PATH"].split(":")


# os.path.abspath(sys.executable)[0] will be None in case of POISX Systems
ROOT_DIR = '/' if os.path.abspath(sys.executable)[0] is None else os.path.abspath(sys.executable)[0]


# scoring variables
SYSTEM_SCORE = 0
TOTAL_SCORE_POSSIBLE = 0


# Supporting DICTIONARIES
SUGGESTIONS_DICT = {}
WARNING_DICT = {}


# Platform System
CURR_SYSTEM_PLATFORM = system().lower()


COMMON_PORTS = {
    23: "TCP",
    234: "UDP"
}

USER_SELECTED_LANGUAGE = None
