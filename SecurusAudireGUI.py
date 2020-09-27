from modules.audit_controller import AuditController
from config import CURR_SYSTEM_PLATFORM, ROOT_DIR
import getpass

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from modules.audits.common import *
from modules.audits.base_model import BaseTest

# UAC elevation
import ctypes
import sys


class CreateCheckBox(Frame):
    def __init__(self, parent_frame, check_box_arrays, starting_row):
        Frame.__init__(self, parent_frame)
        self.vars = {}
        self.starting_row = starting_row
        self.last_row = starting_row
        for i in range(len(check_box_arrays)):
            for j in range(len(check_box_arrays[i])):
                option_value = IntVar()
                audit_name = re.sub(r"(\w)([A-Z])", r"\1 \2", check_box_arrays[i][j].__name__)
                ttk.Checkbutton(parent_frame, variable=option_value, text=f"{audit_name}").grid(
                    column=j,
                    row=starting_row + i + 1,
                    padx=50,
                    sticky=(
                        N, S))
                self.vars[check_box_arrays[i][j]] = option_value
                self.last_row = i + 1

    def get_last_row(self):
        return self.last_row

    def select_all(self):
        for cls, value in self.vars.items():
            value.set(1)

    def clear_all(self):
        for cls, value in self.vars.items():
            value.set(0)

    def state(self):
        return dict(map(lambda x: (x[0], x[1].get()), self.vars.items()))


class SecurusAudireGUI(object):

    def __init__(self):
        self.root = Tk()
        self.root.title('SecurusAudire - A Security Audit Tool')
        self.save_folder_location = ""
        self.audit_classes = {}

    @staticmethod
    def convert_to_matrix(arr: list):
        matrix = []
        for i in range(0, len(arr), 3):
            temp_arr = arr[i:i + 3]
            matrix.append(temp_arr)

        return matrix

    def create_main_frame(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(3, weight=1)

    def create_title_frame(self):
        title_frame = ttk.Frame(self.mainframe, padding="3 3 3 3")
        title_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        # canvas = Canvas(self.root, width=300, height=300).grid(column=1, row=0, sticky=(W, E))

        title = ttk.Label(title_frame, text="SecurusAudire - A Security Audit Tool")
        title.configure(font=("Verdana", 16, "bold"))
        title.grid(column=1, row=0, sticky=(E, W))
        ttk.Label(title_frame, text="                             ").grid(column=0,
                                                                                          row=1, sticky=(N, E, W, S))

    def create_master_audit_frame(self):
        audit_frame = ttk.Frame(self.mainframe, padding="3 3 12 12")
        audit_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        audit_title = ttk.Label(audit_frame, text="Select Audits to perform - ")
        audit_title.configure(font=("Verdana", 14, "bold"))
        audit_title.grid(column=1, row=0, sticky=(W, E))

    def create_general_system_audits_section(self):
        general_system_audits_frame = ttk.Frame(self.mainframe, padding="1 1 12 12")
        general_system_audits_frame.grid(column=0, row=2, sticky=(N, W, E, S))
        audit_type_title = ttk.Label(general_system_audits_frame, text="General System Audits")
        audit_type_title.configure(font=("Verdana", 12, "bold"))
        audit_type_title.grid(column=1, row=0, sticky=(W, E))

        self.audit_classes['general_system_audits'] = BaseTest.__subclasses__()
        general_system_audits = self.convert_to_matrix(self.audit_classes['general_system_audits'])

        self.general_system_audits_check_boxes = CreateCheckBox(parent_frame=general_system_audits_frame,
                                                                check_box_arrays=general_system_audits,
                                                                starting_row=3)
        ttk.Label(general_system_audits_frame, text="                                             ").grid(column=1,
                                                                                                          row=1,
                                                                                                          sticky=(W, E))
        ttk.Button(general_system_audits_frame, text='Select All',
                   command=self.general_system_audits_check_boxes.select_all).grid(column=0,
                                                                                   row=2,
                                                                                   sticky=(W, E))

        ttk.Button(general_system_audits_frame, text='Clear All',
                   command=self.general_system_audits_check_boxes.clear_all).grid(column=2,
                                                                                  row=2,
                                                                                  sticky=(W, E))
        ttk.Label(general_system_audits_frame, text="                                             ").grid(column=1,
                                                                                                          row=3,
                                                                                                          sticky=(W, E))

    def create_system_based_audits_section(self):
        system_based_audits_frame = ttk.Frame(self.mainframe, padding="1 1 12 12")
        system_based_audits_frame.grid(column=0, row=3, sticky=(N, W, E, S))
        audit_title = ttk.Label(system_based_audits_frame, text="System Based Audits")
        audit_title.configure(font=("Verdana", 12, "bold"))
        audit_title.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(system_based_audits_frame, text="                                             ").grid(column=1,
                                                                                                        row=1,
                                                                                                        sticky=(W, E))
        system_title = ttk.Label(system_based_audits_frame, text=f"Showing audits for system type - {CURR_SYSTEM_PLATFORM}")
        system_title.configure(font=("Verdana", 10, "bold"))
        system_title.grid(
            column=1,
            row=2,
            sticky=(W, E))
        ttk.Label(system_based_audits_frame, text="                                             ").grid(column=1,
                                                                                                        row=3,
                                                                                                        sticky=(W, E))
        if CURR_SYSTEM_PLATFORM == "linux":
            import modules.audits.linux
        elif CURR_SYSTEM_PLATFORM == "windows":
            import modules.audits.windows
        else:
            ttk.Label(system_based_audits_frame, text=f"{CURR_SYSTEM_PLATFORM} not supported").grid(column=1, row=0,
                                                                                                    sticky=(W, E))
            return

        self.audit_classes['system_specific_audits'] = [audit_class for audit_class in BaseTest.__subclasses__()
                                                        if
                                                        audit_class not in self.audit_classes['general_system_audits']]

        system_specific_audits = self.convert_to_matrix(self.audit_classes['system_specific_audits'])

        self.system_specific_audits_check_boxes = CreateCheckBox(parent_frame=system_based_audits_frame,
                                                                 check_box_arrays=system_specific_audits,
                                                                 starting_row=5)

        ttk.Button(system_based_audits_frame, text='Select All',
                   command=self.system_specific_audits_check_boxes.select_all).grid(column=0,
                                                                                    row=4,
                                                                                    sticky=(W, E))

        ttk.Button(system_based_audits_frame, text='Clear All',
                   command=self.system_specific_audits_check_boxes.clear_all).grid(column=2,
                                                                                   row=4,
                                                                                   sticky=(W, E))

        ttk.Label(system_based_audits_frame, text="                                             ").grid(column=1,
                                                                                                        row=5,
                                                                                                        sticky=(W, E))

    def create_custom_audits_section(self):
        custom_audit_frame = ttk.Frame(self.mainframe, padding="1 1 12 12")
        custom_audit_frame.grid(column=0, row=4, sticky=(N, W, E, S))
        audit_title = ttk.Label(custom_audit_frame, text="User defined Audits")
        audit_title.configure(font=("Verdana", 12, "bold"))
        audit_title.grid(column=1, row=0, sticky=(W, E))
        ttk.Label(custom_audit_frame, text="                                             ").grid(column=1,
                                                                                                 row=1,
                                                                                                 sticky=(W, E))
        if CURR_SYSTEM_PLATFORM == "linux":
            import modules.audits.linux.custom_audits
        elif CURR_SYSTEM_PLATFORM == "windows":
            import modules.audits.windows.custom_audits
        else:
            ttk.Label(custom_audit_frame, text=f"{CURR_SYSTEM_PLATFORM} not supported").grid(column=1, row=0,
                                                                                             sticky=(W, E))
            return

        self.audit_classes['custom_audits'] = [audit_class for audit_class in BaseTest.__subclasses__()
                                               if
                                               audit_class not in self.audit_classes['general_system_audits']
                                               if
                                               audit_class not in self.audit_classes['system_specific_audits']]

        custom_audits = self.convert_to_matrix(self.audit_classes['custom_audits'])

        if not custom_audits:

            ttk.Label(custom_audit_frame, text=f"No User defined found in the system").grid(column=1, row=2,
                                                                                            sticky=(W, E))
        else:
            self.custom_audits_check_boxes = CreateCheckBox(parent_frame=custom_audit_frame,
                                                            check_box_arrays=custom_audits,
                                                            starting_row=3)

            ttk.Button(custom_audit_frame, text='Select All',
                       command=self.custom_audits_check_boxes.select_all).grid(column=0,
                                                                               row=2,
                                                                               sticky=(W, E))

            ttk.Button(custom_audit_frame, text='Clear All',
                       command=self.custom_audits_check_boxes.clear_all).grid(column=2,
                                                                              row=2,
                                                                              sticky=(W, E))

            ttk.Label(custom_audit_frame, text="                                             ").grid(column=1,
                                                                                                     row=3,
                                                                                                     sticky=(W, E))

    def set_save_directory(self):
        self.save_folder_location = filedialog.askdirectory()

        if len(self.save_folder_location) == 0:

            if CURR_SYSTEM_PLATFORM == "linux":
                self.save_folder_location = "/var/log"

            elif CURR_SYSTEM_PLATFORM == "windows":
                self.save_folder_location = ROOT_DIR

            else:
                pass

        if CURR_SYSTEM_PLATFORM == "windows":
            self.save_folder_location = self.save_folder_location.replace("/", '\\')

        file_entry_widget = ttk.Entry(self.file_save_box_frame, width=50)
        file_entry_widget.grid(column=1, row=1)
        file_entry_widget.insert(0, self.save_folder_location)

    def create_file_save_location_section(self):
        self.file_save_box_frame = ttk.Frame(self.mainframe, padding="1 1 12 12")
        self.file_save_box_frame.grid(column=0, row=5, sticky=(N, W, E, S))

        save_folder_title = ttk.Label(self.file_save_box_frame, text="Report Save Location:")
        save_folder_title.configure(font=("Verdana", 12, "bold"))
        save_folder_title.grid(column=0, row=1, padx=10)
        ttk.Entry(self.file_save_box_frame, width=50).grid(column=2, row=1, padx=10)

        ttk.Button(self.file_save_box_frame, text="Browse", command=self.set_save_directory).grid(column=3, row=1, padx=10)

    def create_driver_buttons_section(self):
        driver_buttons_frame = ttk.Frame(self.mainframe, padding="1 1 12 12")
        driver_buttons_frame.grid(column=0, row=6, sticky=(N, W, E, S))

        ttk.Button(driver_buttons_frame, text="Start System Audit", command=self.run_audit).grid(column=2, row=1, padx=30)

        ttk.Button(driver_buttons_frame, text="Exit", command=self.exit_gui).grid(column=3, row=1, padx=30)

    def set_audits_status(self):
        categories_state = [self.general_system_audits_check_boxes.state(),
                            self.system_specific_audits_check_boxes.state()]
        try:
            categories_state.append(self.custom_audits_check_boxes.state())
        except AttributeError:
            categories_state.append({})

        no_audit_check_flag = False

        for category in categories_state:
            for audit, state in category.items():
                if state == 1:
                    no_audit_check_flag = True
                    break

        if no_audit_check_flag:
            for category in categories_state:
                for audit, state in category.items():
                    if state == 0:
                        audit.__disabled__ = True
            return True

        return False

    def run_audit(self):
        audits_to_run = self.set_audits_status()

        if audits_to_run:
            audit_controller_object = AuditController(self.save_folder_location)
            audit_status = audit_controller_object.controller()
            if audit_status == 5:
                messagebox.showinfo('Info', 'OS Not Supported as of now')
                self.exit_gui()
            elif audit_status == 0:
                messagebox.showinfo('Success',
                                    'System Audit Complete. You can view generated reports at - ' +
                                    self.save_folder_location + "/SecurusAudire_Reports/")
                self.exit_gui()
            else:
                result = messagebox.askyesno('Error',
                                             'SecurusAudire encountered some errors, are you running the script as '
                                             'root?')
                if not result:
                    messagebox.showinfo('Info', 'Script should be executed with root privileges!!!')
                    self.exit_gui()
                else:
                    messagebox.showinfo('Info', 'Please exit and try again!!!')
                    self.exit_gui()
        else:
            messagebox.showinfo('Error', 'No audits have been selected, please select an audit and run the program '
                                         'again!!!')
            self.run_gui()

    def run_gui(self):
        self.create_main_frame()

        self.create_title_frame()

        self.create_master_audit_frame()

        self.create_general_system_audits_section()

        self.create_system_based_audits_section()

        self.create_custom_audits_section()

        self.create_file_save_location_section()

        self.create_driver_buttons_section()

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.root.mainloop()

    def exit_gui(self):
        self.root.destroy()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":

    if CURR_SYSTEM_PLATFORM == "windows":

        if is_admin():
            # check if user is admin, if True then run audit
            # else re run program with admin privileges
            gui_obj = SecurusAudireGUI()
            gui_obj.run_gui()

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    gui_obj = SecurusAudireGUI()
    gui_obj.run_gui()
