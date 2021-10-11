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

    direcPrimary = "D:/~Dropbox/Dropbox/Pictures/General/Art/Moe/"
    direcSecondary = "D:/~Dropbox/Dropbox/Pictures/Phone Copy/Art/Moe/"
    diff = files.dirDiff(direcPrimary, direcSecondary)

    print("%d file(s) differ between the given directories" % len(diff))

    if not os.path.isdir("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/Art/Moe/"):
        os.makedirs("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/Art/Moe/")

    dirTransfer = "D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/Art/Moe/"
    for file in diff:
        name = list(os.path.split(file))
        logger.debug(name[1])

        copyLoc = files.locateFile("D:/~Dropbox/Dropbox/Pictures/Phone Copy/", 5, name[1])
        if len(copyLoc) == 0:
            shutil.copy2(os.path.join("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/Art/Moe/", file), os.path.join(dirTransfer, name[1]), follow_symlinks=True)
        elif len(copyLoc) == 1:
            # TODO move file in primary directory to match secondary directory

            path = os.path.split(copyLoc[0])[0].replace("D:/~Dropbox/Dropbox/Pictures/Phone Copy", "") + "/"
            print(path)
            
            #shutil.copy2()
            pass

        #print(name[1])
    pass

    # files.locateFile("D:/~Dropbox/Dropbox/Pictures/General/Art/", 5, "00IQMG8.png")

if __name__ == "__main__":
    app()
