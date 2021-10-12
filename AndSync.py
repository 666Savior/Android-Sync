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

    fh.setLevel(logging.INFO)

    direcPrimary= "D:/~Dropbox/Dropbox/Pictures/General/"
    direcSecondary = "D:/~Dropbox/Dropbox/Pictures/Phone Copy/"
    diff = files.dirDiff(direcPrimary, direcSecondary)

    print("%d file(s) differ between the given directories" % len(diff))

    if not os.path.isdir("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/"):
        os.makedirs("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/")

    dirTransfer = "D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/"
    for file in diff:
        name = list(os.path.split(file))
        logger.debug(name[1])

        copyLoc = files.locateFile("D:/~Dropbox/Dropbox/Pictures/Phone Copy/", 5, name[1])
        logger.debug(len(copyLoc))
        logger.debug(copyLoc)

        if len(copyLoc) == 0:
            shutil.copy2(os.path.join("D:/~Dropbox/Dropbox/Pictures/General/", file), os.path.join(dirTransfer, name[1]), follow_symlinks=True)
        elif len(copyLoc) == 1:

            logger.info(copyLoc[0])
            path = os.path.split(copyLoc[0])[0].replace("D:/~Dropbox/Dropbox/Pictures/Phone Copy\\", "") + "/"
            path = path.replace("\\", "/")

            logger.debug(name[1])
            logger.info(path)
            logger.debug(os.path.join("D:/~Dropbox/Dropbox/Pictures/General/", path))

            if not os.path.isdir(os.path.join("D:/~Dropbox/Dropbox/Pictures/General/", path)):
                os.makedirs(os.path.join("D:/~Dropbox/Dropbox/Pictures/General/", path))

            shutil.copy2(src=file, dst=os.path.join("D:/~Dropbox/Dropbox/Pictures/General/", os.path.join(path, name[1])), follow_symlinks=True)
            shutil.copy2(src=file, dst=os.path.join("D:/~Dropbox/Dropbox/Pictures/To Delete/", name[1]), follow_symlinks=True)
            os.remove(file)


if __name__ == "__main__":
    app()
