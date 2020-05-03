from config import CURR_SYSTEM_PLATFORM


class AuditController:
    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        
    def controller(self):
        
        if CURR_SYSTEM_PLATFORM == "linux":

            from modules.audits.linux.linux_controller import LinuxAuditController

            linux_audit_controller_object = LinuxAuditController(save_folder_location=self.save_folder_location)
            audit_result = linux_audit_controller_object.controller()
        
        elif CURR_SYSTEM_PLATFORM == "windows":
            from modules.audits.windows.windows_controller import WindowsAuditController

            windows_audit_controller_object = WindowsAuditController(save_folder_location=self.save_folder_location)
            audit_result = windows_audit_controller_object.controller()

        else:

            audit_result = 5

        return audit_result
