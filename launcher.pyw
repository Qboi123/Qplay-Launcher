import os
import zipfile
import wx
from threading import Thread
from time import sleep

import wx
import wx.html2


def replace_dir2ver(string: str):
    return string.replace("_pre", "-pre").replace("_", ".")


def replace_ver2dir(string: str):
    return string.replace("-pre", "_pre").replace(".", "_")


def replace_name2dir(string: str):
    return replace_ver2dir(replace_name2ver(string))


def replace_name2ver(string: str):
    return string.replace(" Pre-Release ", "-pre")


def replace_any2name(ver: str):
    ver = replace_dir2ver(ver)
    return ver.replace("-pre", " Pre-Release ")


def ver2list(string: str):
    if string.count(".") == 0:
        replace_dir2ver(string)
    string = string[1:]
    string.split(".")


def extract_zipfile(path2zip: str, extract_path: str):
    zip_ref = zipfile.ZipFile(path2zip, 'r')
    zip_ref.extractall(extract_path)
    zip_ref.close()


def speed():
    import time
    global active
    global spd
    global h, m, s
    while active:
        total1 = total
        time.sleep(1)
        total2 = total
        spd = (total2 - total1) * 1
        try:
            a = (fileTotalbytes - total) / spd
            b = time.gmtime(a)
            hours = b[3]
            # noinspection PyShadowingBuiltins
            min = b[4]
            sec = b[5]
        except ZeroDivisionError:
            a = 0
            b = time.gmtime(a)
            hours = b[3]
            # noinspection PyShadowingBuiltins
            min = b[4]
            sec = b[5]
        h = str(hours)
        m = str(min)
        s = str(sec)
        if min < 10:
            m = "0" + m
        if sec < 10:
            s = "0" + s


def download(url: str, panel: wx.Panel, version: str):
    import urllib.request
    from threading import Thread

    global active
    global total
    global spd
    global fileTotalbytes
    global h, m, s
    global load
    h = "23"
    m = "59"
    s = "59"
    spd = 0
    total = 0

    # Get the total number of bytes of the file to download before downloading
    u = urllib.request.urlopen(str(url))
    if os.path.exists("temp/QplayBubbles-" + version + '.zip'):
        os.remove("temp/QplayBubbles-" + version + '.zip')
    meta = u.info()
    fileTotalbytes = int(meta["Content-Length"])

    data_blocks = []
    total = 0

    frame.Show(False)

    load = wx.ProgressDialog("Downloading...", "Download from Qplay123/Qplay-Bubbles", maximum=100)

    active = True

    Thread(None, lambda: speed(), "SpeedThread").start()

    while True:
        block = u.read(1024)
        data_blocks.append(block)
        total += len(block)
        _hash = ((60 * total) // fileTotalbytes)
        frame.Update()
        panel.Update()
        load.Update(int(total / fileTotalbytes * 100), "Downloading...\nDownloading of \"Qplay123/Qplay-Bubbles\" is " +
                    str(
            int(total / fileTotalbytes * 100)) + "% complete.\n\n" + str(total) + " of " + str(fileTotalbytes) + "\n" +
                     "With "+str(spd)+" bytes/sec | "+h+":"+m+":"+s+" remaining.")

        if not len(block):
            active = False
            break

        try:
            with open("temp/QplayBubbles-" + version + '.zip', "ab+") as f:
                f.write(block)
                f.close()
        except FileNotFoundError:
            os.makedirs("temp/")
            with open("temp/QplayBubbles-" + version + '.zip', "ab+") as f:
                f.write(block)
                f.close()

    # data = b''.join(data_blocks)
    u.close()

    if not os.path.exists("temp"):
        os.makedirs("temp")

    frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
    load.Destroy()
    frame.Show(True)


class Launcher(wx.Panel):
    def __init__(self, master: wx.Frame, *args):
        super().__init__(master, *args)
        import urllib.request, urllib.error

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
            vertical_box = wx.BoxSizer(wx.VERTICAL)

            self.inet_available = True

            _all = list(self.old.keys())+list(self.all.keys())
            _all_build = list(self.old.values())+list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir = os.listdir("versions/")
            dir_build = list()

            for i in dir:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir)):
                i = dir[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            dzf = _all.copy()

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == replace_ver2dir(k):
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
                            _all.insert(j, replace_dir2ver(i))
                            _all_build.insert(j, dir_data[i])
                            found = 1
                            break
                if found == 0:
                    # print("Found\n")
                    if not_exists:
                        _all.append(replace_dir2ver(i))
                        _all_build.append(dir_data[i])
            all = list()
            for i in _all:
                all.append(replace_any2name(i))

            all_build = _all_build
            all_data = _all_data

        except urllib.error.URLError:
            with open("current.json", "w+") as file:
                json_data = file.read()
            self.data = json.JSONDecoder().decode(json_data)

            with open("all_versions.json", "w+") as file:
                json_data = file.read()
            self.all = json.JSONDecoder().decode(json_data)

            with open("old_versions.json", "w+") as file:
                json_data = file.read()
            self.old = json.JSONDecoder().decode(json_data)

            # ------------------------------------------------------------------------------------------------------------ #
            vertical_box = wx.BoxSizer(wx.VERTICAL)

            self.inet_available = False


            _all = list(self.old.keys())+list(self.all.keys())
            _all_build = list(self.old.values())+list(self.all.values())
            # print(_all)
            # print(_all_build)
            dir = os.listdir("versions/")
            dir_build = list()

            for i in dir:
                with open("versions/%s/version.json" % i) as file:
                    versionData = json.JSONDecoder().decode(file.read())
                    dir_build.append(versionData["build"])

            dir_data = dict()
            for _i in range(len(dir)):
                i = dir[_i]
                j = dir_build[_i]
                dir_data[i] = j

            _all_data = dict()
            for _i in range(len(_all)):
                i = _all[_i]
                j = _all_build[_i]
                _all_data[i] = j

            # print(dir_data)
            # print(_all)

            dzf = _all.copy()

            for i in os.listdir("versions/"):
                # print("I: %s" % i)
                for k in _all:
                    # print("K: %s" % k)
                    if i == replace_ver2dir(k):
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
                            _all.insert(j, replace_dir2ver(i))
                            _all_build.insert(j, dir_data[i])
                            found = 1
                            break
                if found == 0:
                    # print("Found\n")
                    if not_exists:
                        _all.append(replace_dir2ver(i))
                        _all_build.append(dir_data[i])
            all = list()
            for i in _all:
                all.append(replace_any2name(i))

            all_build = _all_build
            all_data = _all_data



            # all = list(self.old.keys()) + list(self.all.keys())
            # all.sort(reverse=True)

        all.reverse()


        self.versions = wx.Choice(self, pos=(0, 640-35), choices=all)
        self.versions.SetSelection(0)
        self.browser = wx.html2.WebView
        self.page = self.browser.New(self, size=(1265, 600))
        self.page.LoadURL("https://quintenjungblut.wixsite.com/qplaysoftware/qplay-bubbles-changelog")
        self.play = wx.Button(self, label="Play!", size=wx.Size(120, 70), pos=(640-60, 640-35))
        self.play.Bind(wx.EVT_BUTTON, lambda event: self.open())
        self.play.Show()

        self.SetSizer(vertical_box)

    def open(self):
        import sys, json

        version = replace_name2ver(self.versions.GetString(self.versions.GetSelection()))
        if version == "":
            return

        version_dir = replace_ver2dir(version)

        print(version_dir)

        if version in self.old:
            if not os.path.exists("versions/" + version_dir + "/"):
                download(
                    "https://github.com/Qplay123/QplayBubbles-OldReleases/archive/" + version + ".zip",
                    self, version
                )
                extract_zipfile("temp/QplayBubbles-" + version + '.zip', "versions/")
                os.rename("versions/QplayBubbles-OldReleases-" + version[1:], "versions/" + version_dir)
                build = self.old[version]
                a = {'build': build, 'displayName': replace_any2name(version)}
                with open("versions/%s/version.json" % version_dir, "w+") as file:
                    file.write(json.JSONEncoder().encode(a))
        else:
            if not os.path.exists("versions/" + version_dir + "/"):
                download(
                    "https://github.com/Qplay123/QplayBubbles-Releaes/archive/" + version + ".zip",
                    self, version
                )
                extract_zipfile("temp/QplayBubbles-" + version + '.zip', "versions/")
                os.rename("versions/QplayBubbles-Releaes-" + version[1:], "versions/" + version_dir)
                build = self.all[version]
                a = {'build': build, 'displayName': replace_any2name(version)}
                with open("versions/%s/version.json" % version_dir, "w+") as file:
                    file.write(json.JSONEncoder().encode(a))

        if not os.path.exists("mods/%s" % version_dir):
            os.makedirs("mods/%s" % version_dir)

        cfg = {"version": version,
               "versionDir": version_dir,
               "launcher": self,
               "args": sys.argv
               }

        print(os.curdir)
        a = __import__("versions.%s.__main__" % version_dir, fromlist=["__main__"])
        if version > "v1.4.1":
            b = Thread(None, lambda: a.Game(launcher_cfg=cfg))
            b.start()
        elif version >= "v1.0.0":
            a.Game()
        else:
            pass


if __name__ == '__main__':
    if not os.path.exists("versions"):
        os.makedirs("versions")
    if not os.path.exists("mods"):
        os.makedirs("mods")
    if not os.path.exists("slots"):
        os.makedirs("slots")

    app = wx.App()
    frame = wx.Frame(None, size=wx.Size(1280, 720), pos=wx.Point(0, 2), title="Qplay Bubbles Launcher",
                     style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    main = Launcher(frame)
    frame.Show()
    app.MainLoop()
