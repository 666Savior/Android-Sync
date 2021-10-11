# --------------[Library Import]-------------- #
import logging
import logging.handlers
import queue
import re
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

    for file in diff:
        print(file)
    pass


if __name__ == "__main__":
    app()
