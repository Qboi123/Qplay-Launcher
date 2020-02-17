from threading import Thread
from tkinter import ttk

from threadsafe_tkinter import *


class Download:
    def __init__(self, url, fp="", isTemp=False):
        self.isTemp = isTemp
        self._url = url
        self._fp = fp
        self.file_total_bytes = 1
        self.file_downloaded_bytes = 0
        self.downloaded: bool = False

        Thread(None, self.download).start()

    # noinspection PyUnboundLocalVariable
    def download(self):
        import urllib.request
        import os
        import tempfile

        self.downloaded = False

        global active
        global total
        global spd
        global h, m, s
        global load
        h = "23"
        m = "59"
        s = "59"
        spd = 0
        total = 0

        dat = None

        while dat is None:
            # Get the total number of bytes of the file to download before downloading
            u = urllib.request.urlopen(str(self._url))
            if os.path.exists(self._fp):
                os.remove(self._fp)
            meta = u.info()
            dat = meta["Content-Length"]
        self.file_total_bytes = int(dat)

        data_blocks = []
        total = 0

        # Thread(None, lambda: speed(), "SpeedThread").start()

        if not os.path.exists(os.path.split(self._fp)[0]):
            os.makedirs(os.path.split(self._fp)[0])

        if self.isTemp:
            with tempfile.TemporaryFile("ab+") as f:
                print(f.file)
                while True:
                    block = u.read(1024)
                    data_blocks.append(block)
                    self.file_downloaded_bytes += len(block)
                    _hash = ((60 * self.file_downloaded_bytes) // self.file_total_bytes)
                    if not len(block):
                        active = False
                        break
                    f.write(block)
                f.close()

        else:
            with open(self._fp, "ab+") as f:
                while True:
                    block = u.read(1024)
                    data_blocks.append(block)
                    self.file_downloaded_bytes += len(block)
                    _hash = ((60 * self.file_downloaded_bytes) // self.file_total_bytes)
                    if not len(block):
                        active = False
                        break
                    f.write(block)
                f.close()

        # data = b''.join(data_blocks)
        u.close()

        if not os.path.exists("temp"):
            os.makedirs("temp")

        self.downloaded = True


class Launcher(Canvas):
    def __init__(self, root, width, height):
        self.width = width
        self.height = height

        super().__init__(root, highlightthickness=0, height=self.height, width=self.width)
        self.root = root
        from lib import utils
        import urllib.request
        import urllib.error
        import os, json

        import sys

        args = sys.argv
        if len(args) > 1:
            for i in args[1:]:
                if i[:12] == "runtime-dir=":
                    self.runtime_dir = i[12:]
                else:
                    print("WARNING: Argument %s has no effect" % i)
        else:
            if os.path.exists(os.path.split(sys.executable)[0]):
                self.runtime_dir = os.path.split(sys.executable)[0]
            else:
                raise RuntimeError("Runtime was not found.")

        try:

            # -- current ------------------------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/current.json"
            )
            json_data = json_url.read().decode()
            with open("current.json", "w+") as file:
                file.write(json_data)

            import json

            self.data = json.JSONDecoder().decode(json_data)
            # print(self.data)

            # -- all versions -------------------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://github.com/Qplay123/Qplay-Bubbles/raw/master/all_versions.json"
            )
            json_data = json_url.read().decode()
            with open("all_versions.json", "w+") as file:
                file.write(json_data)
            with open("all_versions.json", "w") as file:
                file.write(json_data)

            import json

            self.all = json.JSONDecoder().decode(json_data)

            # -- old / historic versions --------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/old_versions.json"
            )
            json_data = json_url.read().decode()

            with open("old_versions.json", "w+") as file:
                file.write(json_data)

            import json

            self.old = json.JSONDecoder().decode(json_data)

            # ------------------------------------------------------------------------------------------------------------ #
            self.inet_available = True

            _all = list(self.old.keys()) + list(self.all.keys())
            _all_build = list(self.old.values()) + list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir_ = os.listdir("versions/")
            dir_build = list()

            for i in dir_:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir_)):
                i = dir_[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == utils.replace_ver2dir(k):
                        not_exists = False
                        break
                    else:
                        not_exists = True

                # print("ALL: %s" % _all)
                found = 0
                for j in range(len(_all_build.copy())):
                    # noinspection PyUnboundLocalVariable
                    if dir_data[i] < _all_build[j] and not_exists:
                        _all.insert(j, utils.replace_dir2ver(i))
                        _all_build.insert(j, dir_data[i])
                        found = 1
                        break
                if found == 0 and not_exists:
                    _all.append(utils.replace_dir2ver(i))
                    _all_build.append(dir_data[i])
            all_ = list()
            for i in _all:
                all_.append(utils.replace_any2name(i))
        except urllib.error.URLError or urllib.error.HTTPError as e:
            self.inet_err = e.args
            print("Error: %s" % e.args[0])
            with open("all_versions.json", "r") as file:
                json_data = file.read()
            self.all = json.JSONDecoder().decode(json_data)

            with open("old_versions.json", "r") as file:
                json_data = file.read()
            self.old = json.JSONDecoder().decode(json_data)

            # ------------------------------------------------------------------------------------------------------------ #
            self.inet_available = False

            _all = list(self.old.keys()) + list(self.all.keys())
            _all_build = list(self.old.values()) + list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir_ = os.listdir("versions/")
            dir_build = list()

            for i in dir_:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir_)):
                i = dir_[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == utils.replace_ver2dir(k):
                        not_exists = False
                        break
                    else:
                        not_exists = True

                # print("ALL: %s" % _all)
                found = 0
                for j in range(len(_all_build.copy())):
                    # print("DirData: %s | AllBuild: %s | All: %s" % (dir_data[i], _all_build[j], _all[j]))
                    if dir_data[i] < _all_build[j]:
                        if not_exists:
                            _all.insert(j, utils.replace_dir2ver(i))
                            _all_build.insert(j, dir_data[i])
                            found = 1
                            break
                if found == 0:
                    # print("Found\n")
                    if not_exists:
                        _all.append(utils.replace_dir2ver(i))
                        _all_build.append(dir_data[i])
            all_ = list()
            for i in _all:
                all_.append(utils.replace_any2name(i))

            # all = list(self.old.keys()) + list(self.all.keys())
            # all.sort(reverse=True)
        all_.reverse()

        self.dir_data = dir_data

        self.pack()
        self.update()

        cUrl = urllib.request.urlopen("https://quintenjungblut.wixsite.com/qplaysoftware/qplay-bubbles-changelog")
        self.changelog = cUrl.read()

        self.imgBottomPanel = utils.openbackground("data/bottomPanel.png", (self.width, 100))
        self.idBottomPanel = self.create_image(0, self.height - 100, image=self.imgBottomPanel, anchor=NW)

        self.imgPlayButtonNormal = utils.openimage("data/playButtonNormal.png")
        self.imgPlayButtonHover = utils.openimage("data/playButtonHover.png")
        self.imgPlayButtonPressed = utils.openimage("data/playButtonPressed.png")
        self.idPlayButton = self.create_image(self.width / 2, self.height - 50, image=self.imgPlayButtonNormal)
        self.tag_bind(self.idPlayButton, "<Enter>", lambda event: self.onPlayButtonEnter())
        self.tag_bind(self.idPlayButton, "<Leave>", lambda event: self.onPlayButtonLeave())
        self.tag_bind(self.idPlayButton, "<ButtonPress-1>", lambda event: self.onPlayButtonPress())
        self.tag_bind(self.idPlayButton, "<ButtonRelease-1>", lambda event: self.onPlayButtonRelease())

        import tkinter as _tk

        def print_choice(event):
            print(self.choice_var.get())  # prints value based on choice var
            print(event)  # prints selection directly from the event passed by the command in OptionMenu

        working_list = list(all_)
        self.choice_var = _tk.StringVar(value=all_[0])
        self.omVersion = _tk.OptionMenu(self.root, self.choice_var, *working_list, command=print_choice)
        print(self.omVersion.keys())
        self.omVersion.configure(background="#FFD800", activebackground="#FFE65E", relief=FLAT, highlightthickness=0,
                                 bd=0)
        self.omVersion["menu"].configure(bg="#3f3f3f", fg="#efefef", bd=0, borderwidth=0, activebackground="#FFD800",
                                         activeforeground="#3f3f3f", relief=FLAT)
        self.omVersion.place(x=5, y=self.height - 50, anchor=W)

        webLoadThread = Thread(None, lambda: self.changeLogLoad(), name="WebLoadThread")
        webLoadThread.start()

        self.update()
        print("%sx%s" % (self.winfo_width(), self.winfo_height()))

    def reload(self):
        self.omVersion.destroy()
        del self.choice_var
        import urllib.request
        import urllib.error
        from lib import utils
        import json
        try:
            # -- current ------------------------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/current.json"
            )
            json_data = json_url.read().decode()
            with open("current.json", "w+") as file:
                file.write(json_data)

            import json

            self.data = json.JSONDecoder().decode(json_data)
            # print(self.data)

            # -- all versions -------------------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://github.com/Qplay123/Qplay-Bubbles/raw/master/all_versions.json"
            )
            json_data = json_url.read().decode()
            with open("all_versions.json", "w+") as file:
                file.write(json_data)
            with open("all_versions.json", "w") as file:
                file.write(json_data)

            import json

            self.all = json.JSONDecoder().decode(json_data)

            # -- old / historic versions --------------------------------------------------------------------------------- #
            json_url = urllib.request.urlopen(
                "https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/old_versions.json"
            )
            json_data = json_url.read().decode()

            with open("old_versions.json", "w+") as file:
                file.write(json_data)

            import json

            self.old = json.JSONDecoder().decode(json_data)

            # ------------------------------------------------------------------------------------------------------------ #
            self.inet_available = True

            _all = list(self.old.keys()) + list(self.all.keys())
            _all_build = list(self.old.values()) + list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir_ = os.listdir("versions/")
            dir_build = list()

            for i in dir_:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir_)):
                i = dir_[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == utils.replace_ver2dir(k):
                        not_exists = False
                        break
                    else:
                        not_exists = True

                # print("ALL: %s" % _all)
                found = 0
                for j in range(len(_all_build.copy())):
                    # noinspection PyUnboundLocalVariable
                    if dir_data[i] < _all_build[j] and not_exists:
                        _all.insert(j, utils.replace_dir2ver(i))
                        _all_build.insert(j, dir_data[i])
                        found = 1
                        break
                if found == 0 and not_exists:
                    _all.append(utils.replace_dir2ver(i))
                    _all_build.append(dir_data[i])
            all_ = list()
            for i in _all:
                all_.append(utils.replace_any2name(i))
        except urllib.error.URLError or urllib.error.HTTPError as e:
            self.inet_err = e.args
            print("Error: %s" % e.args[0])
            with open("all_versions.json", "r") as file:
                json_data = file.read()
            self.all = json.JSONDecoder().decode(json_data)

            with open("old_versions.json", "r") as file:
                json_data = file.read()
            self.old = json.JSONDecoder().decode(json_data)

            # ------------------------------------------------------------------------------------------------------------ #
            self.inet_available = False

            _all = list(self.old.keys()) + list(self.all.keys())
            _all_build = list(self.old.values()) + list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir_ = os.listdir("versions/")
            dir_build = list()

            for i in dir_:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir_)):
                i = dir_[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == utils.replace_ver2dir(k):
                        not_exists = False
                        break
                    else:
                        not_exists = True

                # print("ALL: %s" % _all)
                found = 0
                for j in range(len(_all_build.copy())):
                    # print("DirData: %s | AllBuild: %s | All: %s" % (dir_data[i], _all_build[j], _all[j]))
                    if dir_data[i] < _all_build[j]:
                        if not_exists:
                            _all.insert(j, utils.replace_dir2ver(i))
                            _all_build.insert(j, dir_data[i])
                            found = 1
                            break
                if found == 0:
                    # print("Found\n")
                    if not_exists:
                        _all.append(utils.replace_dir2ver(i))
                        _all_build.append(dir_data[i])
            all_ = list()
            for i in _all:
                all_.append(utils.replace_any2name(i))

            # all = list(self.old.keys()) + list(self.all.keys())
            # all.sort(reverse=True)
        all_.reverse()

        def print_choice(event):
            print(self.choice_var.get())  # prints value based on choice var
            print(event)  # prints selection directly from the event passed by the command in OptionMenu

        working_list = list(all_)
        self.choice_var = StringVar(value=all_[0])
        self.omVersion = OptionMenu(self.root, self.choice_var, *working_list, command=print_choice)
        print(self.omVersion.keys())
        self.omVersion.configure(background="#FFD800", activebackground="#FFE65E", relief=FLAT, highlightthickness=0,
                                 bd=0)
        self.omVersion["menu"].configure(bg="#3f3f3f", fg="#efefef", bd=0, borderwidth=0, activebackground="#FFD800",
                                         activeforeground="#3f3f3f", relief=FLAT)
        self.omVersion.place(x=5, y=self.height - 50, anchor=W)
        self.update()


    def onSelectVersion(self, event):
        print('----------------------------')
        print("event.widget:", event.widget.get())
        print('----------------------------')

    def changeLogLoad(self):
        import urllib.request as urllib
        from lib import utils
        try:
            a = urllib.urlopen("https://github.com/Qplay123/Qplay-Bubbles/raw/master/changelog.qplaylog")
            data = a.read().decode()

            lines = data.split("\n")

            height = -10
            for line in lines:
                if line[:1] == "#":
                    height += 28
                else:
                    height += 24
            height -= 16

            height += 10

            print("%sx%s" % (self.width, height))
            print("%sx%s" % (self.width, self.height - 105))

            s_frame = Frame(self.root, width=self.width, height=self.height - 105)
            # s_frame.place(x=0, y=0)

            sw = utils.ScrolledWindow(s_frame, width=self.width - 9, heigh=height, canv_h=self.height - 100,
                                      canv_w=self.width, scrollcommand=self.scroll)

            canv = sw.canv

            frame = sw.scrollwindow

            self.canvass = Canvas(frame, highlightthickness=0)

            height = -10
            for line in lines:
                if line[:1] == "#":
                    height += 20
                    self.canvass.create_text(10, height, text=line[1:], font=("Helvetica", 28, "bold"), fill="darkgray",
                                             anchor=NW)
                    height += 38
                else:
                    if line.lower()[:5] == "note:":
                        self.canvass.create_text(10, height, text=line, font=("Helvetica", 16), fill="red", anchor=NW)
                        height += 24
                    else:
                        self.canvass.create_text(10, height, text=line, font=("Helvetica", 16), fill="darkgray",
                                                 anchor=NW)
                        height += 24

            height -= 16
            height += 10

            # y1, y2 = sw.vbar.get()
            #
            # print(y1, y2)
            # y1 = y1 * height
            # y2 = y2 * height
            #
            # print(y1, y2)

            self.canvass.config(height=height, width=self.width)
            self.canvass.pack(fill=Y)

            self.cHeight = height

            self.create_window(0, 0, window=s_frame, height=self.height - 100, width=self.width, anchor=NW)

            self.old_value = 25

            print("[sw.scrollwindow]: %sx%s" % (sw.scrollwindow.winfo_width(), sw.scrollwindow.winfo_height()))
            print("[sw.canv]: %sx%s" % (sw.canv.winfo_width(), sw.canv.winfo_height()))
            print("[s_frame]: %sx%s" % (s_frame.winfo_width(), s_frame.winfo_height()))
            print("[canvas2]: %sx%s" % (self.canvass.winfo_width(), self.canvass.winfo_height()))
            self.root.update()
            self.root.update_idletasks()
            self.sw = sw
            print("Ready")
        except urllib.HTTPError or urllib.URLError:
            pass

    def scroll(self, i, reqHeight, vbarValue, vbar: ttk.Scrollbar):
        pass  # The code was never good working. (Impossible to make it for me!!!)
        print("vbarValue", vbarValue)
        value = -i / 1.4
        # a1 = int(self.canvass.coords(self.scroll2)[1]) == 5
        # a2 = value > 0
        # a = not(a1 ^ a2)
        #
        # b1 = ((self.canvass.coords(self.scroll2)[3] > self.cHeight))
        # b2 = value < 0
        # b = not(b1 ^ b2)
        # print(value, value < 0)
        # print(a1, 5)
        # print("====")
        # print(a1, a2)
        # print(a)
        # print("----")
        # print(b1, b2)
        # print(b)
        # print("====\n\n")
        # print("OK")
        x1, y1, x2, y2 = self.canvass.coords(self.scroll2)
        # _y1, _y2 = vbarValue
        # print("1:",y1, y2)
        # print("2:",_y1, _y2)
        # print("3:",(_y2 - _y1) / 2 - y2)
        # print("4:",(_y1 + (_y2 - _y1) / 120) * self.cHeight)
        # print("5:",(_y1 + (_y2 - _y1) / 120) * self.cHeight - (y2 / y1))
        # print("6:",((_y2 - _y1) / 120) * self.cHeight - y2* -i)
        # print("7:",(_y1 + (_y2 - _y1) / 120))
        # value = (_y1 + (_y2 - _y1) / 120) * self.cHeight / (y1 / y2)
        # print("8:",(y2 / y1))
        # # value = value - (y1 / y2)
        #
        # print("Dynamic Canvas Region Height:")
        # print("DCRH:", self.cHeight)
        #
        #
        # print("Value: %s", value)

        print("vbar.identify(*value):", vbar.fraction(int(vbarValue[0] * self.canvass.winfo_height())))

        self.scroll_canv.set(*vbarValue)

        # value = self.canvass.winfo_height() / (value * 41.4)
        #
        # if vbarValue[0] <= 0:
        #     return
        # if vbarValue[1] >= 1:
        #     return
        #
        # self.canvass.move(self.scroll2, 0, -value)
        # self.old_value = value
        print("\n")
        print("value: %s" % value)
        print("coords: %s" % self.canvass.coords(self.scroll2))
        print("reqHeight: %s" % reqHeight)

    def onPlayButtonEnter(self):
        self.itemconfig(self.idPlayButton, image=self.imgPlayButtonHover)

    def onPlayButtonLeave(self):
        self.itemconfig(self.idPlayButton, image=self.imgPlayButtonNormal)

    def onPlayButtonPress(self):
        self.itemconfig(self.idPlayButton, image=self.imgPlayButtonPressed)

    def onPlayButtonRelease(self):
        from lib import utils
        self.itemconfig(self.idPlayButton, image=self.imgPlayButtonHover)
        # self.selectedProfile
        self.version = utils.replace_name2ver(self.choice_var.get())
        self.start()

    def start(self):
        from os.path import exists
        from lib import utils
        import os
        import subprocess as sp
        # fp = "temp/QplayBubbles-" + self.version + '.zip'
        _dir = utils.replace_ver2dir(self.version)
        if not exists("versions/%s" % _dir):
            self.download()

        if not os.path.exists("mods/%s" % _dir):
            os.makedirs("mods/%s" % _dir)

        print("Starting Version: %s" % _dir)
        cfg = {"version": self.version,
               "versionDir": _dir,
               "build": self.dir_data[_dir],
               "runtimeDir": self.runtime_dir
               }

        print("Current Directory: %s" % os.curdir)

        # if self.dir_data[_dir] < 16:
        #     self.root.destroy()

        if self.dir_data[_dir] >= 16:
            exit_code = os.system("{runtimeDir}/python.exe versions/" + _dir + "/__main__.py {version} {versionDir} {build}".format(
                **cfg))
            if exit_code != 0:
                sp.run(("{runtimeDir}/python.exe versions/" + _dir + "/__main__.py {version} {versionDir} {build}".format(
                    **cfg)).split(" "), shell=True)
        else:
            exit_code = os.system("{runtimeDir}/python.exe old_load.py {version} {versionDir} {build}".format(_dir, **cfg))
            if exit_code != 0:
                sp.run(("{runtimeDir}/python.exe old_load.py {version} {versionDir} {build}".format(_dir, **cfg)).split(" "))

    def download(self):
        from os.path import exists
        import os
        import json
        from lib import utils
        fp = "temp/QplayBubbles-" + self.version + '.zip'
        _dir = utils.replace_ver2dir(self.version)

        if not exists("versions/%s" % _dir):
            self.tag_unbind(self.idPlayButton, "<Enter>")
            self.tag_unbind(self.idPlayButton, "<Leave>")
            self.tag_unbind(self.idPlayButton, "<ButtonPress-1>")
            self.tag_unbind(self.idPlayButton, "<ButtonRelease-1>")
            self.omVersion.place_forget()
            self.itemconfig(self.idPlayButton, state=HIDDEN)
            if self.version in self.old:
                down = Download("https://github.com/Qplay123/QplayBubbles-OldReleases/archive/" + self.version + ".zip",
                                "temp/QplayBubbles-" + self.version + '.zip', False)
            else:
                if self.version >= "v1.4.0":
                    down = Download("https://github.com/Qplay123/QplayBubbles-Releaes/archive/" + self.version + ".zip",
                                    "temp/QplayBubbles-" + self.version + '.zip', False)
                elif self.version >= "v1.0.0":
                    down = Download("https://github.com/Qplay123/Qplay-Bubbles/archive/" + self.version + ".zip",
                                    "temp/QplayBubbles-" + self.version + '.zip', False)
                else:
                    down = Download(
                        "https://github.com/Qplay123/QplayBubbles-OldReleases/archive/" + self.version + ".zip",
                        "temp/QplayBubbles-" + self.version + '.zip', False)

            # Thread(None, lambda: down.download()).start()
            self.idDownloadBar = self.create_image(5, self.height - 50, anchor=W)
            self.idDownloadBarLoaded = self.create_image(7, self.height - 50, anchor=W)

            img = utils.openresized("data/downloadBar/unloadedPart.png", (1270, 28))
            self.itemconfig(self.idDownloadBar, image=img)
            while not down.downloaded:
                try:
                    img = utils.openresized("data/downloadBar/unloadedPart.png", (1270, 28))
                    self.itemconfig(self.idDownloadBar, image=img)

                    loadedWidth = int(down.file_downloaded_bytes / down.file_total_bytes * (1280 - 14))
                    img2 = utils.openresized("data/downloadBar/loadedPart.png", (loadedWidth, 24))
                    self.itemconfig(self.idDownloadBarLoaded, image=img2)
                    self.update()
                    self.update_idletasks()

                except ZeroDivisionError:
                    pass
                except ValueError:
                    pass
                except AttributeError:
                    pass

            if self.version in self.old:
                utils.extract_zipfile("temp/QplayBubbles-" + self.version + '.zip', "versions/")
                os.rename("versions/QplayBubbles-OldReleases-" + self.version[1:], "versions/" + _dir)
                build = self.old[self.version]
                a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                with open("versions/%s/version.json" % _dir, "w+") as file:
                    file.write(json.JSONEncoder().encode(a))
            else:
                if self.version >= "v1.4.0":
                    utils.extract_zipfile("temp/QplayBubbles-" + self.version + '.zip', "versions/")
                    os.rename("versions/QplayBubbles-Releaes-" + self.version[1:], "versions/" + _dir)
                    build = self.all[self.version]
                    a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                    with open("versions/%s/version.json" % _dir, "w+") as file:
                        file.write(json.JSONEncoder().encode(a))
                elif self.version >= "v1.0.0":
                    utils.extract_zipfile("temp/QplayBubbles-" + self.version + '.zip', "versions/")
                    os.rename("versions/Qplay-Bubbles-" + self.version[1:], "versions/" + _dir)
                    build = self.all[self.version]
                    a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                    with open("versions/%s/version.json" % _dir, "w+") as file:
                        file.write(json.JSONEncoder().encode(a))

            if os.path.exists("versions/%s/requirements.txt" % _dir):
                with open("versions/%s/requirements.txt" % _dir, "r"):
                    requirements = file.read()
                    file.close()
                if requirements:
                    self.install_libraries(requirements)

            self.itemconfig(self.idPlayButton, state=NORMAL)
            self.itemconfig(self.idDownloadBar, state=HIDDEN)
            self.itemconfig(self.idDownloadBarLoaded, state=HIDDEN)
            self.tag_bind(self.idPlayButton, "<Enter>", lambda event: self.onPlayButtonEnter())
            self.tag_bind(self.idPlayButton, "<Leave>", lambda event: self.onPlayButtonLeave())
            self.tag_bind(self.idPlayButton, "<ButtonPress-1>", lambda event: self.onPlayButtonPress())
            self.tag_bind(self.idPlayButton, "<ButtonRelease-1>", lambda event: self.onPlayButtonRelease())

            self.omVersion.place(x=5, y=self.height - 50, anchor=W)

            self.reload()

    def install_libraries(self, requirements: str):
        requirements = requirements.replace("\n", " ")
        os.system("%s/python.exe -m pip install %s" % (self.runtime_dir, requirements))


if __name__ == '__main__':
    import os

    if not os.path.exists("versions"):
        os.makedirs("versions")
    if not os.path.exists("mods"):
        os.makedirs("mods")
    if not os.path.exists("slots"):
        os.makedirs("slots")

    width = 1280
    height = 720
    tk = Tk()
    style = ttk.Style(tk)
    style.theme_use('clam')

    # configure the style
    style.configure("Horizontal.TScrollbar", gripcount=0,
                    background="#3f3f3f", darkcolor="#3f3f3f", lightcolor="LightGreen",
                    troughcolor="gray", bordercolor="blue", arrowcolor="white")

    tk.overrideredirect(False)
    tk.wm_resizable(False, False)
    tk.geometry("%sx%s" % (width, height))
    Launcher(tk, width, height)
    tk.mainloop()
