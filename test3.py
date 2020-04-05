from lib import utils
import yaml
import os

fd = os.open("lang/en.yaml", os.O_RDONLY | os.O_CREAT)
y = yaml.safe_load(os.read(fd, 4096).decode())
os.close(fd)

utils.yamldict2class(y)