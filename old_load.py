import sys, os


cfg = {"version": sys.argv[1],
       "versionDir": sys.argv[2],
       "build": sys.argv[3],
       "file": sys.argv[0]}

version = cfg["version"]
_dir = cfg["versionDir"]

print(cfg)

sys.path.append("%s/versions/%s" % (os.getcwd().replace("\\", "/"), _dir))
sys.path.append("%s/" % (os.getcwd().replace("\\", "/")))

if version > "v1.4.1":
    sys.path.append("%s/" % (os.getcwd().replace("\\", "/")))
    a = __import__("versions.%s.__main__" % _dir, fromlist=["__main__"])
    if hasattr(a, "Initialize"):
        a.Game(launcher_cfg=cfg)
    else:
        a.Game(launcher_cfg=cfg)
elif version >= "v1.4.0":
    sys.path.append("%s/" % (os.getcwd().replace("\\", "/")))
    a = __import__("versions.%s.__main__" % _dir, fromlist=["__main__"])
    os.chdir("versions/%s/" % _dir)
    a.Game()
elif version >= "v1.0.0":
    import time

    # print(os.getcwd())
    # print("%s/versions/%s/" % (os.getcwd().replace("\\", "/"), _dir))
    # exit(1)
    sys.path.append("%s/versions/%s/" % (os.getcwd().replace("\\", "/"), _dir))
    os.chdir("versions/%s/" % _dir)
    a = __import__("__main__" % _dir, fromlist=["__main__"])
    a.Game(time.time())
    # self.__init__(self.root, self.width, self.height)
    os.chdir("../../")
