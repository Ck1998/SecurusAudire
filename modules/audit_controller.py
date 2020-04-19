from platform import system


class AuditController:
    def __init__(self, save_folder_location):
        super().__init__()
        self.save_folder_location = save_folder_location
        
    def controller(self):
        current_system = system()
        if current_system.lower() == "linux":

        
            from modules.audits.linux.linux_controller import LinuxAuditController

            linux_audit_controller_object = LinuxAuditController(save_folder_location=self.save_folder_location)
            audit_result = linux_audit_controller_object.controller()
        
        elif current_system.lower() == "windows":

            from modules.audits.windows.windows_controller import WindowsAuditController

            windows_audit_controller_object = WindowsAuditController(save_folder_location=self.save_folder_location)
            audit_result = windows_audit_controller_object.controller()
        else:
            audit_result = 5
            
        return audit_result
