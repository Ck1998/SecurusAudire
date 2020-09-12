from tkinter import *
from tkinter import ttk

"""def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


def hp():
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    feet = StringVar()
    meters = StringVar()

    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind('<Return>', calculate)"""


class CreateCheckBox(Frame):
    def __init__(self, parent_frame, check_box_arrays, starting_row):
        Frame.__init__(self, parent_frame)
        self.vars = {}
        self.starting_row = starting_row
        self.last_row = starting_row
        for i in range(len(check_box_arrays)):
            for j in range(len(check_box_arrays[i])):
                option_value = IntVar()
                ttk.Checkbutton(parent_frame, variable=option_value, text=f"{arr[i][j]}").grid(column=j,
                                                                                               row=starting_row + i + 1,
                                                                                               sticky=(N, S))
                self.vars[arr[i][j]] = option_value
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
        print(dict(map(lambda x: (x[0], x[1].get()), self.vars.items())))


if __name__ == "__main__":
    root = Tk()
    root.title('SecurusAudire - A Security Audit Tool')

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(3, weight=1)
    root.rowconfigure(3, weight=1)

    # Title Frame
    title_frame = ttk.Frame(mainframe, padding="3 3 12 12")
    title_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    ttk.Label(title_frame, text="SecurusAudire").grid(column=1, row=0, sticky=(W, E))
    ttk.Label(title_frame, text="2020").grid(column=1, row=1, sticky=(W, E))

    # Audit Frame
    audit_frame = ttk.Frame(mainframe, padding="3 3 12 12")
    audit_frame.grid(column=0, row=1, sticky=(N, W, E, S))

    ttk.Label(audit_frame, text="Select Audits").grid(column=1, row=0, sticky=(W, E))

    # general system audits
    general_system_audits_frame = ttk.Frame(mainframe, padding="1 1 12 12")
    general_system_audits_frame.grid(column=0, row=2, sticky=(N, W, E, S))

    arr = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["10"]]
    ttk.Label(general_system_audits_frame, text="general system audits").grid(column=1, row=0, sticky=(W, E))

    gene = CreateCheckBox(parent_frame=general_system_audits_frame, check_box_arrays=arr, starting_row=1)

    ttk.Button(general_system_audits_frame, text='Select All', command=gene.select_all).grid(column=0,
                                                                                             row=1,
                                                                                             sticky=(W, E))

    ttk.Button(general_system_audits_frame, text='Clear All', command=gene.clear_all).grid(column=2,
                                                                                           row=1,
                                                                                           sticky=(W, E))
    general_system_audit_last_row = gene.last_row
    ttk.Button(general_system_audits_frame, text='Peek', command=gene.state).grid(column=1,
                                                                                  row=general_system_audit_last_row + 2,
                                                                                  sticky=(W, E))

    # System based audits
    system_based_audits_frame = ttk.Frame(mainframe, padding="1 1 12 12")
    system_based_audits_frame.grid(column=0, row=3, sticky=(N, W, E, S))

    arr = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["10", "11", "12"]]
    ttk.Label(system_based_audits_frame, text="system based audits").grid(column=1, row=0, sticky=(W, E))

    system_based_audits = CreateCheckBox(parent_frame=system_based_audits_frame, check_box_arrays=arr, starting_row=1)
    system_based_audits_row = system_based_audits.last_row
    Button(system_based_audits_frame, text='Peek', command=system_based_audits.state).grid(column=1,
                                                                                           row=system_based_audits_row + 2,
                                                                                           sticky=(W, E))

    # custom audits
    custom_audit_frame = ttk.Frame(mainframe, padding="1 1 12 12")
    custom_audit_frame.grid(column=0, row=4, sticky=(N, W, E, S))

    arr = []
    ttk.Label(custom_audit_frame, text="custom sddff audits").grid(column=1, row=0, sticky=(W, E))

    custom_audits = CreateCheckBox(parent_frame=custom_audit_frame, check_box_arrays=arr, starting_row=1)
    custom_audits_last_row = custom_audits.last_row
    Button(custom_audit_frame, text='Peek', command=custom_audits.state).grid(column=1,
                                                                              row=system_based_audits_row + 2,
                                                                              sticky=(W, E))

    """ttk.Checkbutton(general_system_audits_frame, text="1").grid(column=1, row=1, sticky=(W, E))
    ttk.Checkbutton(general_system_audits_frame, text="2").grid(column=2, row=1, sticky=(W, E))
    ttk.Checkbutton(general_system_audits_frame, text="3").grid(column=3, row=1, sticky=(W, E))
    ttk.Checkbutton(general_system_audits_frame, text="4").grid(column=1, row=2, sticky=(W, E))"""
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.mainloop()

"""
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        if len(picks)%3 == 0:
            no_of_rows = int(len(picks)/3)
        else:
            no_of_rows = int((len(picks) / 3) + 1)
        initial_count = 0
        for row in range(no_of_rows):
            for pick in picks[initial_count:initial_count+3]:
                var = IntVar()
                chk = Checkbutton(self, text=pick, variable=var)
                chk.pack(side=side, anchor=anchor, expand=YES)
                self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


if __name__ == '__main__':
    root = Tk()
    lng = Checkbar(root, ['Python', 'Ruby', 'Perl', 'C++', 'Python', 'Ruby', 'Perl', 'C++'])
    tgl = Checkbar(root, ['English', 'German'])
    lng.pack(side=TOP, fill=X)
    tgl.pack(side=LEFT)
    lng.config(relief=GROOVE, bd=2)


    def allstates():
        print(list(lng.state()), list(tgl.state()))


    Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    root.mainloop()"""
