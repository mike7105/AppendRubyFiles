# -*- coding: utf-8 -*-
"""AppendRubyFiles start"""
__version__ = 'Version:1.3'
import traceback
import tkinter as tk
import tkinter.messagebox as msgbox
from modules.application import Application
# import sys
# import os

# def resource_path(relative_path):
#    """ Get absolute path to resource, works for dev and for PyInstaller """
#    base_path = getattr(sys, '_MEIPASS',
#       os.path.dirname(os.path.abspath(__file__)))
#    return os.path.join(base_path, relative_path)

# image_path = resource_path("cd.ico")

ROOT = tk.Tk()
try:
    APP = Application(master=ROOT, version=__version__)
    # ROOT.iconbitmap(image_path)
    # ROOT.wm_state('zoomed')
    ROOT.mainloop()
except BaseException:
    trace_inf = traceback.format_exc()
    print("Unexpected error:", trace_inf)  # sys.exc_info()[0])
    msgbox.showinfo("Unexpected error:", trace_inf)
    # sys.exc_info()[0], parent=ROOT)
# finally:
    # input("Нажмите для выхода...")
