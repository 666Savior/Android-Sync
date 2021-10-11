# --------------[Library Import]-------------- #
import logging
import logging.handlers
import os.path
import queue
import re
import shutil
import threading
import time

# --------------[Custom Module Import]-------------- #
import StateCache
import files

# --------------[Logger Initialize]-------------- #
logger = logging.getLogger('AndSync')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler('C:\\Users\\Public\\Documents\\AndSync\\AndSync.log',
                                          maxBytes=10000000,
                                          backupCount=5)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s || %(levelname)s | %(name)s -| %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def app():
    diff = files.dirDiff("D:/~Dropbox/Dropbox/Pictures/General/Art/Moe/",
                         "D:/~Dropbox/Dropbox/Pictures/General/Art/Moe - Copy/")

    if not os.path.isdir("D:/~Dropbox/Dropbox/Pictures/General/Art/Moe - Needs Transfer/"):
        os.makedirs("D:/~Dropbox/Dropbox/Pictures/General/Art/Moe - Needs Transfer/")

    dirTransfer = "D:/~Dropbox/Dropbox/Pictures/General/Art/Moe - Needs Transfer/"
    for file in diff:
        name = list(os.path.split(file))
        logger.debug(name[1])

        shutil.copy(file, os.path.join(dirTransfer, name[1]), follow_symlinks=True)
        #print(name[1])
    pass


if __name__ == "__main__":
    app()
