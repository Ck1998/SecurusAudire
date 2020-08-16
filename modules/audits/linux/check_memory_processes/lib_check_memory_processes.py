from modules.audits.base_model import BaseTest
from psutil import STATUS_ZOMBIE, STATUS_DEAD, process_iter

# config variables
import config as CONFIG


class CheckMemoryProcesses(BaseTest):

    __disabled__ = False

    def __init__(self):
        super().__init__()
        self.test_result = {}

    def check_dead_and_zombie_process(self):
        self.test_result["Zombie Processes"] = {
            "Process Count": 0,
            "Process List": []
        }
        self.test_result["Dead Processes"] = {
            "Process Count": 0,
            "Process List": []
        }
        zombie_process_count = 0
        dead_process_count = 0
        running_process = process_iter()

        for process in running_process:
            process_status = (process.status() if hasattr(process.status, '__call__'
                                                          ) else process.status)

            if process_status == STATUS_ZOMBIE:
                pid = (process.pid() if hasattr(process.pid, '__call__') else process.pid)
                name = (process.name() if hasattr(process.name, '__call__') else process.name)
                zombie_process_count += 1
                self.test_result["Zombie Processes"]["Process List"].append({
                    "Process ID": pid,
                    "Process Name": name
                })

                CONFIG.TOTAL_SCORE_POSSIBLE += 1
                CONFIG.WARNING_DICT[name] = {
                    "Warning": "Zombie Process",
                    "Process ID": pid,
                    "Process Name": name,
                    "Description": "A zombie process or defunct process is a process that has completed execution but "
                                   "still has an entry in the process table.",
                    "Mitigation": f"Execute the following command in the terminal: kill -s SIGCHLD {pid}"
                }

            elif process_status == STATUS_DEAD:
                pid = (process.pid() if hasattr(process.pid, '__call__') else process.pid)
                name = (process.name() if hasattr(process.name, '__call__') else process.name)
                dead_process_count += 1
                self.test_result["Dead Processes"]["Process List"].append({
                    "Process ID": pid,
                    "Process Name": name
                })

                CONFIG.TOTAL_SCORE_POSSIBLE += 1
                CONFIG.WARNING_DICT[name] = {
                    "Warning": "Dead Process",
                    "Process ID": pid,
                    "Process Name": name,
                    "Description": "A zombie process or defunct process is a process that has completed execution but "
                                   "still has an entry in the process table.",
                    "Mitigation": f"Execute the following command in the terminal: kill -s SIGKILL {pid}"
                }
            else:
                CONFIG.SYSTEM_SCORE += 1
                CONFIG.TOTAL_SCORE_POSSIBLE += 1

        self.test_result["Zombie Processes"]["Process Count"] = zombie_process_count
        self.test_result["Dead Processes"]["Process Count"] = dead_process_count

        if zombie_process_count == 0:
            self.test_result["Zombie Processes"]["Process List"] = "No zombie processes found"
        if dead_process_count == 0:
            self.test_result["Dead Processes"]["Process List"] = "No dead processes found"

    def run_test(self):
        self.check_dead_and_zombie_process()
        return self.test_result
