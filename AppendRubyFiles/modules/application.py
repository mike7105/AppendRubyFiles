# -*- coding: utf-8 -*-
"""AppendRubyFiles GUI"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as tkFD
import os
import time
import threading
import queue
import glob
import shutil
import pickle

class Application(ttk.Frame):
    """класс для отрисовки AppendRubyFiles"""
    def __init__(self, master=None, version=""):
        super().__init__(master)
        self.master = master
        self.version = version
        self.grid_params = {"padx": 5, "pady": 5}
        self.grid(row=0, column=0, columnspan=2, sticky="wnse", **self.grid_params)

        self.frame1 = ttk.Frame()
        self.frame1.grid(row=0, column=0, columnspan=2, sticky="wnse", **self.grid_params)

        # ButtonRun
        self.btn_run = ttk.Button(text="Run", command=self.run_append)
        self.btn_run.grid(row=1, column=0, sticky="es", **self.grid_params)

        # ButtonExit
        self.btn_exit = ttk.Button(text="Exit", command=self.master.destroy)
        self.btn_exit.grid(row=1, column=1, sticky="es", **self.grid_params)

        # ProgressBar
        self.var_pb = tk.IntVar()
        self.pgb = ttk.Progressbar(maximum=100, variable=self.var_pb)
        self.var_pb.set(0)
        self.pgb.grid(row=2, column=0, columnspan=2, sticky="we")

        # LabelStatus
        self.var_status = tk.StringVar()
        self.var_status.set("")
        self.lbl_status = ttk.Label(textvariable=self.var_status, relief=tk.RIDGE)
        self.lbl_status.grid(row=3, column=0, columnspan=2, sticky="wes")

        # Sizegrip
        self.sgp = ttk.Sizegrip()
        self.sgp.grid(row=3, column=1, sticky="es")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=10)
        self.master.grid_columnconfigure(1, weight=1)

        self.master.title("AppendRubyFiles")
        self.master.minsize(width=400, height=300)

        self.create_menu()
        self.create_widgets()

        self.time_start = None
        self.time_end = None
        self.time_dur = None
        self.num_prev = 0
        self.num_same = 0
        self.num_new = 0
        self.cd_files = None
        self.lock = None
        self.que = None
        self.barrier = None
        self.to_copy = None

        # #####STYLE#######
        self.style = ttk.Style()

    def create_menu(self):
        """Создание меню"""
        # Создаем само главное меню и назначаем его окну приложения
        window = self.master
        self.mainmenu = tk.Menu(window, tearoff=False)
        window["menu"] = self.mainmenu

        # Создаем подменю Файл
        self.filemenu = tk.Menu(self.mainmenu, tearoff=False)

        self.filemenu.add_command(
            label="Open settings", accelerator="Ctrl+O", command=self.open_settings)
        self.bind_all("<Control-KeyPress-o>", self.open_settings)

        self.filemenu.add_command(
            label="Save settings", accelerator="Ctrl+S", command=self.save_settings)
        self.bind_all("<Control-KeyPress-s>", self.save_settings)

        self.filemenu.add_separator()

        self.filemenu.add_command(
            label="Exit", accelerator="Ctrl+Q", command=self.master.destroy)
        self.bind_all(
            "<Control-KeyPress-q>", lambda evt: self.btn_exit.invoke())

        self.mainmenu.add_cascade(label="File", menu=self.filemenu)

        # Добавляем меню Настройки в главное меню
        self.thememenu = tk.Menu(self.mainmenu, tearoff=False)

        self.them = tk.StringVar()
        self.them.set("vista")
        self.tharr = [
            "default", "winnative", "clam", "alt", "classic", "vista", "xpnative"]

        for style in self.tharr:
            self.thememenu.add_radiobutton(
                label=style, variable=self.them, value=style,
                command=self.change_theme)
        self.mainmenu.add_cascade(label="Theme", menu=self.thememenu)

        # Создаем подменю Справка
        self.helpmenu = tk.Menu(self.mainmenu, tearoff=False)
        self.helpmenu.add_command(label="About...", command=self.show_info)
        self.mainmenu.add_cascade(label="Help", menu=self.helpmenu)

        # Контекстное меню
        self.contextmenu = tk.Menu(self, tearoff=False)
        self.contextmenu.add_command(label="Copy", command=self.copy)

    def create_widgets(self):
        """создает компненты GUI"""
        # список элементов, которые нужно блокировать
        self.elems = []

        # LabelPrev
        self.lbl_prev = ttk.Label(self.frame1, text="Choose Casedata from previous waves:")
        self.lbl_prev.grid(
            row=0, column=0, columnspan=2, sticky="we", **self.grid_params)

        # EntryPrev
        self.var_prev = tk.StringVar()
        self.var_prev.set("")
        self.ent_prev = ttk.Entry(self.frame1, textvariable=self.var_prev)
        # self.ent_prev.state(["disabled"])
        self.ent_prev.bind(
            "<Button-3>", lambda evt, obj=self.var_prev: self.show_menu(evt, obj))
        self.ent_prev.grid(row=1, column=0, sticky="we", **self.grid_params)
        self.elems.append(self.ent_prev)

        # ButtonPrev
        self.btn_prev = ttk.Button(self.frame1, text="Choose...",
                                   command=lambda: self.open_dir(self.var_prev))
        self.btn_prev.grid(row=1, column=1, sticky="e", **self.grid_params)
        self.elems.append(self.btn_prev)

        # LabelCurr
        self.lbl_curr = ttk.Label(self.frame1, text="Choose Casedata from last wave:")
        self.lbl_curr.grid(
            row=2, column=0, columnspan=2, sticky="we", **self.grid_params)

        # EntryCurr
        self.var_curr = tk.StringVar()
        self.var_curr.set("")
        self.ent_curr = ttk.Entry(self.frame1, textvariable=self.var_curr)
        # self.ent_curr.state(["disabled"])
        self.ent_curr.bind(
            "<Button-3>", lambda evt, obj=self.var_curr: self.show_menu(evt, obj))
        self.ent_curr.grid(row=3, column=0, sticky="we", **self.grid_params)
        self.elems.append(self.ent_curr)

        # ButtonCurr
        self.btn_curr = ttk.Button(self.frame1, text="Choose...",
                                   command=lambda: self.open_dir(self.var_curr))
        self.btn_curr.grid(row=3, column=1, sticky="e", **self.grid_params)
        self.elems.append(self.btn_curr)

        # LabelRes
        self.lbl_res = ttk.Label(self.frame1, text="Choose Casedata for appended waves:")
        self.lbl_res.grid(
            row=4, column=0, columnspan=2, sticky="we", **self.grid_params)

        # EntryRes
        self.var_res = tk.StringVar()
        self.var_res.set("")
        self.ent_res = ttk.Entry(self.frame1, textvariable=self.var_res)
        # self.ent_res.state(["disabled"])
        self.ent_res.bind(
            "<Button-3>", lambda evt, obj=self.var_curr: self.show_menu(evt, obj))
        self.ent_res.grid(row=5, column=0, sticky="we", **self.grid_params)
        self.elems.append(self.ent_res)

        # ButtonRes
        self.btn_res = ttk.Button(self.frame1, text="Choose...",
                                  command=lambda: self.open_dir(self.var_res))
        self.btn_res.grid(row=5, column=1, sticky="e", **self.grid_params)
        self.elems.append(self.btn_res)

        self.frame1.grid_columnconfigure(0, weight=10)
        self.frame1.grid_columnconfigure(1, weight=1)

    def run_append(self):
        """запускает присоединение файлов"""
        self.change_state(False)
        self.var_status.set("")
        self.lbl_status.update()
        if self.validate():
            self.time_start = time.time()
            self.num_prev = 0
            self.num_same = 0
            self.num_new = 0

            # копирую все файлы met
            self.var_status.set("copy met files")
            self.lbl_status.update()
            for met_file in glob.glob(self.var_curr.get() + "\\*.met"):
                shutil.copy(met_file, self.var_res.get())

            self.cd_files = glob.glob(self.var_curr.get() + "\\*.cd")
            self.pgb["maximum"] = len(self.cd_files)

            if os.path.exists(os.path.join(self.var_prev.get(), "id.cd")):
                self.num_prev = self.count_lines(os.path.join(self.var_prev.get(), "id.cd"))

            self.var_status.set("copy cd files")
            self.lbl_status.update()
            self.lock = threading.Lock()
            self.que = queue.Queue()

            # прохожусь по всем cd файлам self.var_curr
            for cd_file_c in self.cd_files:
                self.que.put(cd_file_c)

            # запуская многопоточное дозаписывание файлов
            threads = []
            quant_bariers = len(self.cd_files)
            quant_bariers = 500 if quant_bariers > 500 else quant_bariers
            self.barrier = threading.Barrier(quant_bariers)
            for i in range(0, quant_bariers-1):
                thr = threading.Thread(target=self.run_append_th)
                threads.append(thr)
                thr.start()
            thr = threading.Thread(target=self.thread_end)
            threads.append(thr)
            thr.start()
        else:
            self.change_state(True)

    def run_append_th(self):
        """запускает присоединение файлов в многопоточном режиме"""
        local = threading.local()
        while not self.que.empty():
            local.cd_file_c = self.que.get()
            local.cd_file_p = os.path.join(self.var_prev.get(), os.path.split(local.cd_file_c)[1])

            # если в self.var_prev есть такой же файл, то его копирую и
            # дописываю содержимым файла из self.var_curr
            if os.path.exists(local.cd_file_p):
                self.num_same += 1
                if self.num_prev == 0:
                    self.num_prev = self.count_lines(local.cd_file_p)

                local.cd_file_r = shutil.copy(local.cd_file_p, self.var_res.get())

                with open(local.cd_file_c, 'rb') as local.fsrc:
                    with open(local.cd_file_r, 'ab') as local.fdst:
                        shutil.copyfileobj(local.fsrc, local.fdst)
                        with self.lock:
                            self.var_status.set(os.path.basename(local.cd_file_r))
                            self.lbl_status.update()
                            self.pgb.step()

            # если файла нет, то нужно создать пустой с определенным кол-вом строк
            else:
                self.num_new += 1
                local.cd_file_r = os.path.join(self.var_res.get(),
                                               os.path.split(local.cd_file_c)[1])

                with open(local.cd_file_r, 'w') as local.f:
                    local.f.write('\n' * self.num_prev)

                with open(local.cd_file_c, 'rb') as local.fsrc:
                    with open(local.cd_file_r, 'ab') as local.fdst:
                        shutil.copyfileobj(local.fsrc, local.fdst)
                        with self.lock:
                            self.var_status.set(os.path.basename(local.cd_file_r))
                            self.lbl_status.update()
                            self.pgb.step()

            self.que.task_done()
        self.barrier.wait()

    def thread_end(self):
        """Функция для завершающего потока"""
        self.barrier.wait()
        self.time_end = time.time()
        self.time_dur = self.time_end - self.time_start
        self.var_status.set("same files {0}; new files {1}; duration {2:.3f}".format(
            self.num_same, self.num_new, self.time_dur))
        self.lbl_status.update()
        self.change_state(True)

    def count_lines(self, filename, chunk_size=1<<13):
        """считает кол-во строк в файле"""
        with open(filename) as file:
            chunk = '\n'
            nlines = 0
            for chunk in iter(lambda: file.read(chunk_size), ''):
                nlines += chunk.count('\n')
        return nlines + (not chunk.endswith('\n'))

    def open_dir(self, obj):
        """Выбор директории"""
        self.var_status.set("")
        filename = tkFD.askdirectory()
        if filename:
            obj.set(filename)
        else:
            msgbox.showerror("Choose CaseData folder", "Folder wasn't chosen!")

    def show_info(self):
        """Показ информации"""
        msgbox.showinfo("О программе...", """{0}
        © Михаил Чесноков, 2019 г.
        mailto: Mihail.Chesnokov@ipsos.com""".format(self.version), parent=self)

    def show_menu(self, evt, obj):
        """Показывает контекстное меню"""
        self.to_copy = obj.get()
        self.contextmenu.post(evt.x_root, evt.y_root)

    def copy(self):
        """Копирует содержимое путей"""
        # print(self.to_copy)
        self.clipboard_clear()
        self.clipboard_append(self.to_copy)

    def change_theme(self):
        """меняет внешний вид при выборе встроенных тем"""
        self.style.theme_use(self.them.get())

    def validate(self) -> bool:
        """проверка введенных значений"""
        res = ""
        if not self.var_prev.get():
            res = "Choose previous waves CaseData!\n"
        else:
            if not os.path.exists(self.var_prev.get()):
                res = res + "{0} doesn't exist!\n".format(self.var_prev.get())
        if not self.var_curr.get():
            res = res + "Choose last wave CaseData!\n"
        else:
            if not os.path.exists(self.var_curr.get()):
                res = res + "{0} doesn't exist!\n".format(self.var_curr.get())
        if not self.var_res.get():
            res = res + "Choose result CaseData!"
        else:
            if not os.path.exists(self.var_res.get()):
                res = res + "{0} doesn't exist!\n".format(self.var_res.get())
        if res:
            msgbox.showerror("Validation fail", res)
            return False
        return True

    def change_state(self, is_visible):
        """меняет активность элементов"""
        for elem in self.elems:
            if is_visible:
                if hasattr(elem, 'state'):
                    elem.state(["!disabled"])
                else:
                    elem.config(state="normal")
            else:
                if hasattr(elem, 'state'):
                    elem.state(["disabled"])
                else:
                    elem.config(state="disabled")

    def open_settings(self, evt=None):
        """Считывание сохраненных ранее параметров"""
        filename = tkFD.askopenfilename(
            title="Open settings",
            filetypes=(("Settings", "TXT"),))
        if filename:
            with open(filename, "rb") as fln:
                obj = pickle.load(fln)
                self.var_prev.set(obj[0])
                self.var_curr.set(obj[1])
                self.var_res.set(obj[2])
        else:
            msgbox.showerror(
                title="settings", message="File wasn't chosen!")

    def save_settings(self, evt=None):
        """Сохранение введенных параметров"""
        filename = tkFD.asksaveasfilename(
            title="Save settings", filetypes=(("Settings", "TXT"),))
        if filename:
            with open(filename + ".txt", "wb") as fln:
                obj = [self.var_prev.get(), self.var_curr.get(), self.var_res.get()]
                pickle.dump(obj, fln)
        else:
            msgbox.showerror("settings", "File wasn't chosen!")
if __name__ == "__main__":
    pass
