import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
from modules.audit_controller import AuditController
from config import CURR_SYSTEM_PLATFORM, ROOT_DIR


# UAC elevation
import ctypes
import sys

class SecurusAudireGUI:

    def __init__(self):
        super().__init__()
        self.window = tk.Tk()
        self.window_width = 1000
        self.window_height = 200
        self.window.geometry(str(self.window_width)+"x"+str(self.window_height))
        self.window.title("SecurusAudire - A Security Audit Tool")
        self.save_folder_location = ""

    def set_text_labels(self):

        main_title_label = tk.Label(self.window, text="SecurusAudire - A Security Audit Tool")
        main_title_label.grid(column=0, row=0)

        sub_title_label = tk.Label(self.window, text="2020")
        sub_title_label.grid(column=0, row=1)
    
    def set_buttons(self):
        
        run_audit_button = tk.Button(self.window, text="Run System Audit", command= self.run_audit)
        run_audit_button.grid(column=0, row=7)

        exit_button = tk.Button(self.window, text="Exit", command=self.exit_gui)
        exit_button.grid(column=1, row=7)

    def file_entry_widget(self):
        file_save_title_label = tk.Label(self.window, text="Report Save Location")
        file_save_title_label.grid(column=0, row=4)

        file_entry_text = tk.Entry(self.window, width=50)
        file_entry_text.grid(column=1, row=4)

        file_save_button = tk.Button(self.window, text="Browse", command=self.set_save_directory)
        file_save_button.grid(column=2, row=4)
    
    def set_save_directory(self):
        self.save_folder_location = tk.filedialog.askdirectory()
        print(self.save_folder_location)

        if len(self.save_folder_location) == 0:
            
            if CURR_SYSTEM_PLATFORM == "linux":
                self.save_folder_location = "/var/log"

            elif CURR_SYSTEM_PLATFORM == "windows":
                self.save_folder_location = ROOT_DIR
        else:
            self.save_folder_location = save_folder_location

        
        file_entry_text = tk.Entry(self.window, width=50)
        file_entry_text.grid(column=1, row=4)
        file_entry_text.insert(0, self.save_folder_location)

    def run_audit(self):
        audit_controller_object = AuditController(self.save_folder_location)
        audit_status = audit_controller_object.controller()
        
        if audit_status == 5:
            tk.messagebox.showinfo('Info','OS Not Supported as of now')
            self.exit_gui()
        elif audit_status == 0:
            tk.messagebox.showinfo('Success','System Audit Complete. You can view generated reports at - '+self.save_folder_location+"/SecurusAudire_Reports/")
            self.exit_gui()
        else:
            result = tk.messagebox.askyesno('Error', 'SecurusAudire encountered some errors, are you running the script as root?') 
            if not result:
                tk.messagebox.showinfo('Info','Script should be executed with root privileges!!!')
                self.exit_gui()
            else:
                tk.messagebox.showinfo('Info','Please exit and try again!!!')
                self.exit_gui()

    def run_gui(self):
        self.set_text_labels()
        self.set_buttons()
        self.file_entry_widget()
        self.window.mainloop()

    def exit_gui(self):
        self.window.destroy()

def is_admin():
    try: 
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":

    if CURR_SYSTEM_PLATFORM == "windows":
        
        if is_admin():
            # check if user is admin, if True then run audit
            # else re run program with admin privledges
            gui_obj = SecurusAudireGUI()
            gui_obj.run_gui()

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    elif CURR_SYSTEM_PLATFORM == "linux":

        gui_obj = SecurusAudireGUI()
        gui_obj.run_gui()
    
