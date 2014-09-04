import yaml
import os

class Config():
    def __init__(self, fname="config.yaml"):
        self.load(fname)

    def load(self, fname):
        self.def_home_dir = os.environ.get("MSGSERVER_HOME_DIR", os.getcwd())
        default = os.path.join(self.def_home_dir, "conf", fname)

        self.config = os.environ.get("MSGSERVER_CONFIG", default)
        self.dataMap = yaml.load(open(self.config))

    def dump(self):
        print self.dataMap
