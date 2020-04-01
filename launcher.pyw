import shutil
import xml.etree.ElementTree
from threading import Thread
from tkinter import ttk

from threadsafe_tkinter import *
import wx


class Download:
    # noinspection PySameParameterValue
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

        if not os.path.exists(f"{appdata_path}/temp"):
            os.makedirs(f"{appdata_path}/temp")

        self.downloaded = True


class Updater(wx.Panel):
    def __init__(self, url: str, data: list):
        local_updates = self.get_updates(url)

        import os

        updates = []
        for update in data:
            if update["for"]["product"] != "qbubbles":
                continue
            if update in local_updates:
                continue
            updates.append(update)
        if not updates:
            return
        self.load = wx.ProgressDialog("Downloading Updates", "")
        for update in updates:

        if (not os.path.exists(f"{appdata_path}/lib/")):
            print("")
            launcher = self.download(url, "")
        if not os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Runtime")
            runtime = self.download("https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-amd64.zip",
                                    message="Downloading Runtime")
        if not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Tkinter")
            tkinter = self.download("https://github.com/Qboi123/Tkinter-Python/archive/8.6.9.zip",
                                    message="Downloading Tkinter")
        if not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Downloading Pip Installer")
            pip = self.download("https://bootstrap.pypa.io/get-pip.py", fp="get-pip.py",
                                message="Downloading Pip Installer")

        if (not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/"))) or not checker.isNewest():
            print("[Updater]: Extracting Launcher")
            self.extract(launcher, "%s/game" % os.getcwd().replace("\\", "/"), "Extracting Launcher",
                         "Qplay-Launcher-",
                         v, sv, r, st, stb)
            with open("%s/game/downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Extracting Runtime")
            self.extract(runtime, "%s/runtime" % os.getcwd().replace("\\", "/"), "Extracting Runtime")
            with open("%s/runtime/downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/")):
            print("[Updater]: Extracing Tkinter")
            self.extract(tkinter, "%s/runtime" % os.getcwd().replace("\\", "/"), "Extracting Tkinter",
                         "Tkinter-Python-", 8, 6, 9, 'r')
            with open("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
        if not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/")):
            import shutil
            self.load.SetTitle("Installing...")
            self.load.SetRange(100)
            self.load.Update(0, "Installing...\nInstalling Pip")

            runtime_dir = "%s/runtime" % os.getcwd().replace("\\", "/")

            print("[Updater]: Extracing from './runtime/python37.zip' to './runtime/Lib'")
            self.extract(runtime_dir+"/python37.zip", runtime_dir+"/Lib/", "Extracing...\nExtracting Python Runtime Library")

            exitcode = 1

            print("[Updater]: Executing Pip Installer")
            while exitcode == 1:
                exitcode = os.system("runtime\\python.exe temp/get-pip.py")
            print("Pip exited with code: %s" % exitcode)

            self.load.Update(66, "Installing...\nInstalling Pip")

            self.replace_in_file("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "#import site", "import site")
            self.replace_in_file("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), ".\n",
                                 "./Lib\n./DLLs")
            dlls = """runtime/_sqlite3.pyd
runtime/_lzma.pyd
runtime/_hashlib.pyd
runtime/_decimal.pyd
runtime/select.pyd
runtime/_socket.pyd
runtime/_elementtree.pyd
runtime/_multiprocessing.pyd
runtime/_overlapped.pyd
runtime/_asyncio.pyd
runtime/_msi.pyd
runtime/_queue.pyd
runtime/_ctypes.pyd
runtime/_bz2.pyd
runtime/libcrypto-1_1.dll
runtime/libssl-1_1.dll
runtime/pyexpat.pyd
runtime/_tkinter.pyd
runtime/_ssl.pyd
runtime/tk86t.dll
runtime/tcl86t.dll
runtime/unicodedata.pyd
runtime/winsound.pyd"""
            dlls = dlls.split("\n")
            if not os.path.exists("%s/runtime/DLLs/" % os.getcwd().replace("\\", "/")):
                os.makedirs("%s/runtime/DLLs/" % os.getcwd().replace("\\", "/"))
                self.load.Update(70, "Installing...\nInstalling Pip")

            for file in dlls:
                dst = file.replace("runtime/", "runtime/DLLs/")
                shutil.copy(("%s/"+file) % os.getcwd().replace("\\", "/"), ("%s/"+dst) % os.getcwd().replace("\\", "/"))
            self.load.Update(81, "Installing...\nInstalling Pip")


            if not os.path.exists(runtime_dir+'/Lib/tkinter'):
                shutil.move(runtime_dir+"/tkinter", runtime_dir+"/Lib")
            # with open("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "r") as file:
            #     a = file.read()
            #     self.load.Update(77, "Installing...\nInstalling Pip")
            # with open("%s/runtime/python37._pth" % os.getcwd().replace("\\", "/"), "w") as file:
            #     a = a.replace("#import site", "import site")
            #     file.write(a)
            #     self.load.Update(88, "Installing...\nInstalling Pip")
            # with open("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
            #     file.write("True")

            self.load.Update(82, "Installing...\nInstalling Pip: \nExtracing Python Runtime Library")


            with open("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()

        if (not os.path.exists("%s/game/downloaded" % os.getcwd().replace("\\", "/")) or not (
                os.path.exists("%s/runtime/downloaded" % os.getcwd().replace("\\", "/")))) or (
                not os.path.exists("%s/runtime/tkinter_downloaded" % os.getcwd().replace("\\", "/"))) or (
                not os.path.exists("%s/runtime/pip_installed" % os.getcwd().replace("\\", "/"))):
            self.load.Destroy()

        if (not os.path.exists("%s/game/patched" % os.getcwd().replace("\\", "/")))  or not checker.isNewest():
            print("[Updater]: Patching Launcher")
            add = """import sys, os
sys.path.append(os.getcwd().replace("\\\\", "/"))
"""
            with open("%s/game/launcher.pyw" % os.getcwd().replace("\\", "/"), "r") as file:
                file_launcher = file.read()
            with open("%s/game/launcher.pyw" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write(add + file_launcher)
            with open("%s/game/patched" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()
        if not os.path.exists("%s/runtime/packages_installed" % os.getcwd().replace("\\", "/")):
            with open("%s/game/requirements.txt" % os.getcwd().replace("\\", "/"), "r") as file:
                print("[Updater]: Installing Libraries")
                self.install_libraries(file.read())
                file.close()
            with open("%s/runtime/packages_installed" % os.getcwd().replace("\\", "/"), "w+") as file:
                file.write("True")
                file.close()

        with open("%s/updates.xml" % os.getcwd().replace("\\", "/"), "w+") as file:
            file.write(xml)

    def replace_in_file(self, fp, old, new):
        with open(fp, "r") as file:
            d = file.read()
        with open(fp, "w") as file:
            d = d.replace(old, new)
            file.write(d)

    def extract(self, file, dir, message, folder=None, v=None, sv=None, r=None, st=None, stb=None):
        import zipfile
        import os
        import shutil

        if st == "a":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "alpha", stb)
        elif st == "b":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "beta", stb)
        elif st == "c":
            copy = "%s.%s.%s-%s.%s" % (v, sv, r, "rc", stb)
        elif st == "r":
            copy = "%s.%s.%s" % (v, sv, r)
        else:
            copy = None

        self.load.SetTitle("Extracting...")
        self.load.SetRange(100)
        self.load.Update(0, "Extracing...\n" + message)

        zip_file = zipfile.ZipFile(file)
        if copy is not None:
            print("[Checking]:", folder == "Qplay-Launcher-")
            print("[Checking]:", folder)
            if folder == "Qplay-Launcher-":
                shutil.rmtree('%s/game' % os.getcwd().replace("\\", "/"), ignore_errors=True)
            self.load.Update(1, "Extracing...\n" + message)
            zip_file.extractall("%s/temp" % os.getcwd().replace("\\", "/"))
            self.load.Update(98, "Extracing...\n" + message)
            print(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy), dir)
            if folder == "Tkinter-Python-":
                for item in os.listdir(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy)):
                    shutil.move(("%s/temp/" + folder + "%s/" + item) % (os.getcwd().replace("\\", "/"), copy),
                               dir + "/" + item)
            else:
                shutil.move(("%s/temp/" + folder + "%s") % (os.getcwd().replace("\\", "/"), copy), dir)

            while not os.path.exists(dir):
                time.sleep(1)
        else:
            if not os.path.exists(dir):
                os.makedirs(dir)
            self.load.Update(99, "Extracing...\n" + message)
            zip_file.extractall(dir)

        self.load.Update(100, "Extracing...\n" + message)

    def download(self, url, message="Downloading Launcher", wait=False, fp=None):
        import random
        import os

        self.load.SetTitle("Downloading...")
        self.load.SetRange(100)
        self.load.Update(0, "Downloading...\n" + message)

        value = random.randint(0x100000000000, 0xffffffffffff)
        if fp is None:
            filepath = hex(value)[2:] + ".tmp"
        else:
            filepath = fp

        if not os.path.exists("%s/temp" % os.getcwd().replace("\\", "/")):
            os.makedirs("%s/temp" % os.getcwd().replace("\\", "/"))

        download = Download(url, "%s/temp/%s" % (os.getcwd().replace("\\", "/"), filepath))
        # Thread(None, download.download, "DownloadThread")

        self.load.SetRange(download.file_total_bytes + 1)
        while not download.downloaded:
            # print("Downloaded: ", download.file_downloaded_bytes)
            # print("Total: ", download.file_total_bytes)
            try:
                self.load.SetRange(download.file_total_bytes + 1)
                self.load.Update(download.file_downloaded_bytes, "Downloading...\n" + message)
            except wx._core.wxAssertionError:
                pass

        # load.Destroy()

        return "%s/temp/%s" % (os.getcwd().replace("\\", "/"), filepath)

    def install_libraries(self, requirements: str):
        import os
        import subprocess

        req = requirements.replace("\n", ", ")

        requirements = requirements.replace("\n", " ")
        print("[Run-Pip]: Installing Packages: %s" % req)
        application = '"%s/runtime/python.exe"' % os.getcwd().replace("\\", "/")
        args = " -m pip install "+requirements
        cmd = application+args

        print("[Run-Pip]: %s" % cmd)

        process = os.system(cmd)
        print("[Run-Pip]: Process Returned: %s" % process)
        if process != 0:
            print('[Run-Pip]: Retrying with subprocess...')
            process = subprocess.call([application, "-m", "pip", "install", *requirements.split(" ")])
            while process is None:
                time.sleep(1)
            print("[Run-Pip]: Process Returned: %s" % process)

    def run(self):
        import os
        # import subprocess

        os.chdir("%s/game" % os.getcwd().replace("\\", "/"))

        import subprocess
        file = '%s/../runtime/python.exe' % os.getcwd().replace("\\", "/")
        py = '%s/launcher.pyw' % os.getcwd().replace("\\", "/")
        # print('[Run]: "{file}" "{py}"'.format(file=file, py=py))
        cmd = '"{file}" "{py}"'.format(file=file, py=py)

        print("[Run-Game]: %s" % cmd)

        process = os.system(cmd)
        print("[Run-Game]: Process Returned: %s" % process)
        if process != 0:
            print('[Run-Game]: Retrying with subprocess...')
            subprocess.call([file, py])
            while process is None:
                time.sleep(1)
            print("[Run-Game]: Process Returned: %s" % process)

        # print("[Run]: \"%s/../runtime/python.exe\" \"%s/launcher.pyw\"" % (
        #     os.getcwd().replace("\\", "/"), os.getcwd().replace("\\", "/")))
        #
        # subprocess.run(("%s/../runtime/python.exe"% os.getcwd().replace("\\", "/"),
        #                "%s/launcher.pyw\"" % os.getcwd().replace("\\", "/")), stderr=stderr, stdout=stdout)


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
            if os.path.split(sys.executable)[0]:
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
            dir_ = os.listdir(f"{appdata_path}/versions/")
            dir_build = list()

            for i in dir_:
                with open(f"{appdata_path}/versions/%s/version.json" % i) as file:
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

            for i in os.listdir(f"{appdata_path}/versions/"):
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
            dir_ = os.listdir(f"{appdata_path}/versions/")
            dir_build = list()

            for i in dir_:
                with open(f"{appdata_path}/versions/%s/version.json" % i) as file:
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

            for i in os.listdir(f"{appdata_path}/versions/"):
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
            dir_ = os.listdir(f"{appdata_path}/versions/")
            dir_build = list()

            for i in dir_:
                with open(f"{appdata_path}/versions/%s/version.json" % i) as file:
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

            for i in os.listdir(f"{appdata_path}/versions/"):
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
            dir_ = os.listdir(f"{appdata_path}/versions/")
            dir_build = list()

            for i in dir_:
                with open(f"{appdata_path}/versions/%s/version.json" % i) as file:
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

            for i in os.listdir(f"{appdata_path}/versions/"):
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

    def changeLogLoad(self):
        import urllib.request
        import urllib.error
        from lib import utils
        try:
            a = urllib.request.urlopen("https://github.com/Qplay123/Qplay-Bubbles/raw/master/changelog.qplaylog")
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
                                      canv_w=self.width)

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
        except urllib.error.HTTPError or urllib.error.URLError:
            pass

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
        # fp = f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip'
        _dir = utils.replace_ver2dir(self.version)
        if not exists(f"{appdata_path}/versions/%s" % _dir):
            self.download()

        if not os.path.exists(f"{appdata_path}/mods/%s" % _dir):
            os.makedirs(f"{appdata_path}/mods/%s" % _dir)

        print("Starting Version: %s" % _dir)
        cfg = {"version": self.version,
               "versionDir": _dir,
               "build": self.dir_data[_dir],
               "runtimeDir": self.runtime_dir
               }

        if os.path.exists(f"{appdata_path}/old_load.py"):
            shutil.copy("old_load.py", f"{appdata_path}/old_load.py")

        if os.path.exists(f"{appdata_path}/lang/"):
            shutil.copytree("lang/", f"{appdata_path}/lang/")

        if os.path.exists(f"{appdata_path}/lib/"):
            shutil.copytree("lib/", f"{appdata_path}/lib/")

        oldDir = os.getcwd()
        os.chdir(f"{appdata_path}")

        print("Current Directory: %s" % os.curdir)
        # if self.dir_data[_dir] < 16:
        #     self.root.destroy()

        if self.dir_data[_dir] >= 16:
            # exit_code = os.system("{runtimeDir}/python.exe versions/" + _dir + "/__main__.py {version} {versionDir} {build}".format(
            #     **cfg))
            command = [f"{cfg['runtimeDir']}/python.exe",
                       f"version/{_dir}/__main__.py",
                       f"{cfg['version']}",
                       f"{cfg['versionDir']}",
                       f"{cfg['build']}"]
            sp.Popen(command, shell=True, cwd=appdata_path)
        else:
            # exit_code = os.system("{runtimeDir}/python.exe old_load.py {version} {versionDir} {build}".format(_dir, **cfg))
            command = [f"{cfg['runtimeDir']}/python.exe",
                       f"old_load.py",
                       f"{cfg['version']}",
                       f"{cfg['versionDir']}",
                       f"{cfg['build']}"]
            sp.Popen(command, cwd=appdata_path)
        os.chdir(oldDir)

    def download(self):
        from os.path import exists
        import os
        import json
        from lib import utils
        if not os.path.exists(f"{appdata_path}/temp/"):
            os.makedirs(f"{appdata_path}/temp/")
        
        fp = f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip'
        _dir = utils.replace_ver2dir(self.version)

        if not exists(f"{appdata_path}/versions/%s" % _dir):
            self.tag_unbind(self.idPlayButton, "<Enter>")
            self.tag_unbind(self.idPlayButton, "<Leave>")
            self.tag_unbind(self.idPlayButton, "<ButtonPress-1>")
            self.tag_unbind(self.idPlayButton, "<ButtonRelease-1>")
            self.omVersion.place_forget()
            self.itemconfig(self.idPlayButton, state=HIDDEN)
            if self.version in self.old:
                down = Download("https://github.com/Qplay123/QplayBubbles-OldReleases/archive/" + self.version + ".zip",
                                f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', False)
            else:
                if self.version >= "v1.4.0":
                    down = Download("https://github.com/Qplay123/QplayBubbles-Releaes/archive/" + self.version + ".zip",
                                    f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', False)
                elif self.version >= "v1.0.0":
                    down = Download("https://github.com/Qplay123/Qplay-Bubbles/archive/" + self.version + ".zip",
                                    f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', False)
                else:
                    down = Download(
                        "https://github.com/Qplay123/QplayBubbles-OldReleases/archive/" + self.version + ".zip",
                        f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', False)

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
                utils.extract_zipfile(f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', f"{appdata_path}/versions/")
                os.rename(f"{appdata_path}/versions/QplayBubbles-OldReleases-" + self.version[1:], f"{appdata_path}/versions/" + _dir)
                build = self.old[self.version]
                a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                with open(f"{appdata_path}/versions/%s/version.json" % _dir, "w+") as file:
                    file.write(json.JSONEncoder().encode(a))
            else:
                if self.version >= "v1.4.0":
                    utils.extract_zipfile(f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', f"{appdata_path}/versions/")
                    os.rename(f"{appdata_path}/versions/QplayBubbles-Releaes-" + self.version[1:], f"{appdata_path}/versions/" + _dir)
                    build = self.all[self.version]
                    a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                    with open(f"{appdata_path}/versions/%s/version.json" % _dir, "w+") as file:
                        file.write(json.JSONEncoder().encode(a))
                elif self.version >= "v1.0.0":
                    utils.extract_zipfile(f"{appdata_path}/temp/QplayBubbles-" + self.version + '.zip', f"{appdata_path}/versions/")
                    os.rename(f"{appdata_path}/versions/Qplay-Bubbles-" + self.version[1:], f"{appdata_path}/versions/" + _dir)
                    build = self.all[self.version]
                    a = {'build': build, 'displayName': utils.replace_any2name(self.version)}
                    with open(f"{appdata_path}/versions/%s/version.json" % _dir, "w+") as file:
                        file.write(json.JSONEncoder().encode(a))

            if os.path.exists(f"{appdata_path}/versions/%s/requirements.txt" % _dir):
                with open(f"{appdata_path}/versions/%s/requirements.txt" % _dir, "r"):
                    requirements = file.read()
                    file.close()
                if requirements:
                    self.install_libraries(requirements)

            self.itemconfig(self.idPlayButton, state=NORMAL)
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
    import platform

    if platform.system().lower() == "windows":
        appdata_path = f"C:/Users/{os.getlogin()}/AppData/Roaming/.qbubbles"
    elif platform.system().lower() == "linux":
        appdata_path = f"/home/{os.getlogin()}/.qbubbles"
    elif platform.system().lower() == "osx":
        appdata_path = f"/Users/{os.getlogin()}/.qbubbles"
    else:
        raise RuntimeError(f"Your platform is incompatible ({platform.system()})")

    Updater("v1_5_0_pre5", xml.etree.ElementTree.parse(f"{appdata_path}/library_versions.xml"))

    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)

    if not os.path.exists(f"{appdata_path}/versions"):
        os.makedirs(f"{appdata_path}/versions")
    if not os.path.exists(f"{appdata_path}/mods"):
        os.makedirs(f"{appdata_path}/mods")
    if not os.path.exists("slots"):
        os.makedirs("slots")

    width = 1280
    height = 720
    tk = Tk()
    style = ttk.Style(tk)
    style.theme_use('classic')

    # configure the style
    style.configure("Horizontal.TScrollbar", gripcount=0,
                    background="#3f3f3f", darkcolor="#3f3f3f", lightcolor="LightGreen",
                    troughcolor="gray", bordercolor="blue", arrowcolor="white")

    tk.overrideredirect(False)
    tk.wm_resizable(False, False)
    tk.geometry("%sx%s" % (width, height))
    Launcher(tk, width, height)
    mainloop()
