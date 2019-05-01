import os
import zipfile

import wx

# a.v1_3_0.__main__.Game()


def replace2ver(string: str):
    return string.replace("_", ".")


def replace2dir(string: str):
    return string.replace(".", "_")


def ver2list(string: str):
    if string.count(".") == 0:
        replace2ver(string)
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
        time.sleep(0.47)
        total2 = total
        spd = (total2 - total1) * 2
        try:
            a = fileTotalbytes / spd
            b = time.gmtime(a)
            hours = b[3]
            min = b[4]
            sec = b[5]
        except ZeroDivisionError:
            a = -1
            b = time.gmtime(a)
            hours = b[3]
            min = b[4]
            sec = b[5]
        h = str(hours)
        m = str(min)
        s = str(sec)
        if min < 10:
            m = "0" + m
        if sec < 10:
            s = "0" + s


def download(url, frame, panel, version):
    import urllib.request
    from threading import Thread

    global active
    global total
    global spd
    global fileTotalbytes
    global h, m, s
    global path_and_file
    global load
    h = "23"
    m = "59"
    s = "59"
    spd = 0
    total = 0
    print(str(url))
    # Get the total number of bytes of the file to download before downloading
    u = urllib.request.urlopen(str(url))
    meta = u.info()
    fileTotalbytes = int(meta["Content-Length"])

    data_blocks = []
    total = 0

    MAX = fileTotalbytes + 1

    # Frame.SetWindowStyle(wx.MINIMIZE | wx.FRAME_NO_TASKBAR)

    # Cancel = wx.Button(Frame, -1, "Cancel")
    # Cancel.Bind(wx.EVT_BUTTON, lambda: app.Destroy())
    #


    # filename.destroy()
    # file_path.destroy()
    # Input.Destroy()

    frame.Show(False)

    load = wx.ProgressDialog("Downloading...", "Download from Qplay123/Qplay-Bubbles", maximum=100)

    # load = ttk.Progressbar(root, length=750, max=MAX)
    # load.config(value=0)
    # load.pack()
    # Frame.Update()

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

    data = b''.join(data_blocks)  # had to add b because I was joining bytes not strings
    u.close()

    if not os.path.exists("temp"):
        os.makedirs("temp")

    with open("temp/QplayBubbles-"+version+'.zip', "wb") as f:
        f.write(data)

    frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
    load.Destroy()
    frame.Show(True)


class Launcher(wx.Panel):
    def __init__(self, master: wx.Frame, *args):
        super().__init__(master, *args)
        import urllib.request

        json_url = urllib.request.urlopen("https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/current.json")
        json_data = json_url.read().decode()

        version = "v1.4.0"
        minimum = "v1.4.0"
        build = 10
        min_build = 10

        import json

        self.data = json.JSONDecoder().decode(json_data)

        if self.data["build"] > build:
            outdated = True
        else:
            outdated = False

        json_url = urllib.request.urlopen("https://raw.githubusercontent.com/Qplay123/Qplay-Bubbles/master/all_versions.json")
        json_data = json_url.read().decode()

        import json

        self.all = json.JSONDecoder().decode(json_data)
        print(self.all)
        for i in ("v1.1.0", "v1.1.1", "v1.2.0-pre1", "v1.2.0-pre2", "v1.2.0", "v1.2.1", "v1.2.2", "v1.3.0-pre1", "v1.3.0"):
            self.all.pop(i)

        print(self.data)
        print(self.all)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        self.versions = wx.Choice(self, pos=(0, 640-35), choices=list(self.all.keys()))
        self.play = wx.Button(self, label="Play!", size=wx.Size(120, 70), pos=(640-60, 640-35))
        self.play.Bind(wx.EVT_BUTTON, self.open)
        self.play.Show()

        self.SetSizer(vertical_box)

    def open(self, event):
        version = self.versions.GetString(self.versions.GetSelection())
        version_dir = replace2dir(version)
        if not os.path.exists("versions/"+version_dir+"/"):
            download("https://codeload.github.com/Qplay123/QplayBubbles-Releaes/zip/"+self.data["version"], frame, self, version)
            extract_zipfile("temp/QplayBubbles-"+version+'.zip', "versions/")
            os.rename("versions/QplayBubbles-Releaes-"+version[1:], "versions/"+version_dir)

        os.chdir("versions/"+version_dir)
        a = __import__("versions.%s.__main__" % version_dir)
        a.__dict__[version_dir].__main__.Game()
        os.chdir("../../")


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, size=wx.Size(1280, 720), title="Qplay Bubbles Launcher")
    main = Launcher(frame)
    frame.Show()
    app.MainLoop()
