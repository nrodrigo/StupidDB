from xml.dom import minidom
import os

class Config:
    def __init__(self):
        self.app_root = os.getcwd()
        config_file = self.app_root+"/config"
        if os.path.isfile(config_file):
            lines = open(config_file).read().splitlines()
            for line in lines:
                if line:
                    get = line.split("=")
                    if get[0] and get[1]:
                        setattr(self, get[0], get[1])
