# -*- coding: utf-8 -*-
"""AppendRubyFiles start"""
__version__ = 'Version:1.5'

import sys
import tkinter as tk
import tkinter.messagebox as msgbox
import traceback

from modules.application import Application, resource_path


ROOT = tk.Tk()
try:
    APP = Application(master=ROOT, version=__version__)
    ROOT.iconbitmap(resource_path(r"modules\ico\cd.ico"))
    # ROOT.wm_state('zoomed')
    ROOT.mainloop()
except Exception as e:
    trace_inf = traceback.format_exc()
    print(e)
    print("Unexpected error:", trace_inf)
    msgbox.showinfo("Unexpected error:", trace_inf)
    ROOT.destroy()
finally:
    sys.exit()
    # input("Нажмите для выхода...")
