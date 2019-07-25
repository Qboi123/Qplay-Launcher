from versions.v1_5_0_pre4.__main__ import Game

if __name__ == '__main__':
    import sys
    cfg = {"version": "v1.5.0-pre4",
           "versionDir": "v1_5_0_pre4",
           "launcher": None,
           "args": sys.argv
           }
    Game(cfg)
