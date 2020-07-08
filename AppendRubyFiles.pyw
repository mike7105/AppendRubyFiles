# -*- coding: utf-8 -*-
"""AppendRubyFiles start"""
__version__ = 'Version:1.4'
import traceback
import tkinter as tk
import tkinter.messagebox as msgbox
from modules.application import Application, resource_path


ROOT = tk.Tk()
try:
    APP = Application(master=ROOT, version=__version__)
    ROOT.iconbitmap(resource_path(r"modules\ico\cd.ico"))
    # ROOT.wm_state('zoomed')
    ROOT.mainloop()
except Exception as e:
    trace_inf = traceback.format_exc()
    print("Unexpected error:", trace_inf)  # sys.exc_info()[0])
    msgbox.showinfo("Unexpected error:", trace_inf)
    # sys.exc_info()[0], parent=ROOT)
# finally:
    # input("Нажмите для выхода...")
