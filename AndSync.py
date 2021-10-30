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

    direcPrimary = "D:/~Dropbox/Dropbox/Pictures/Phone Copy/"
    direcSecondary = "D:/~Dropbox/Dropbox/Pictures/General/"

    trashbin = "D:/~Dropbox/Dropbox/Pictures/To Delete/"

    if not os.path.isdir(trashbin):
        os.makedirs(trashbin)

    foldersPrimary = files.dirFolderScan(direcPrimary)
    foldersSecondary = files.dirFolderScan(direcSecondary)

    # Make sure the secondary directory has the same folders as primary
    files.dirSync(direcPrimary, direcSecondary)

    for folder in foldersPrimary:

        folder = folder.replace("\\", "/").replace(direcPrimary, "")
        logger.debug(folder)

        direcTransfer = os.path.join("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/", folder)
        if not os.path.isdir(os.path.join("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/", folder)):
            os.makedirs(os.path.join("D:/~Dropbox/Dropbox/Pictures/Phone - To Transfer/", folder))

        logger.info(os.path.join(direcPrimary, folder))
        logger.info(os.path.join(direcSecondary, folder))

        diffPrimaryToSecondary = files.dirDiff(os.path.join(direcPrimary, folder), os.path.join(direcSecondary, folder))
        diffSecondaryToPrimary = files.dirDiff(os.path.join(direcSecondary, folder), os.path.join(direcPrimary, folder))

        logger.debug("%d file(s) differ between primary and secondary directory" % len(diffPrimaryToSecondary))
        logger.debug("%d file(s) differ between secondary and primary directory" % len(diffSecondaryToPrimary))

        for file in diffPrimaryToSecondary:
            name = list(os.path.split(file))
            logger.debug(name[1])

            # check for copies in secondary outside of current folder
            copyLoc = files.locateFile(direcSecondary, 5, name[1])
            logger.debug(len(copyLoc))
            logger.debug(copyLoc)

            # If there are no copies anywhere in secondary directory, copy file from primary
            if len(copyLoc) == 0:
                logger.debug(os.path.join(os.path.join(direcPrimary, folder), file))
                logger.debug(os.path.join(os.path.join(direcSecondary, folder), name[1]))
                shutil.copy2(src=os.path.join(os.path.join(direcPrimary, folder), file),
                             dst=os.path.join(os.path.join(direcSecondary, folder), name[1]), follow_symlinks=True)

            # If there is a copy elsewhere in secondary, copy file to match primary directory's file's location
            elif len(copyLoc) == 1:

                src = copyLoc[0]
                dst = os.path.join(os.path.join(direcSecondary, folder), name[1])
                logger.debug(src)
                logger.debug(dst)

                trashFolder = os.path.split(src)[0].replace("\\", "/").replace(direcSecondary, "")
                if not os.path.isdir(os.path.join(trashbin, trashFolder)):
                    os.makedirs(os.path.join(trashbin, trashFolder))

                trashPath = os.path.join(os.path.join(trashbin, trashFolder), name[1]).replace("\\", "/")
                logger.debug(os.path.join(os.path.join(trashbin, trashFolder), name[1]))

                shutil.copy2(src=src, dst=dst, follow_symlinks=True)
                shutil.copy2(src=src, dst=trashPath, follow_symlinks=True)
                #os.remove(src)
            elif len(copyLoc) > 1:
                logger.warning("File found in multiple locations")

        # Loop through any files that the secondary directory has that is not present in primary directory
        if len(diffSecondaryToPrimary) > 0:
            logger.info("Syncing files from secondary")
            for file in diffSecondaryToPrimary:
                name = list(os.path.split(file))
                logger.debug(name[1])

                # Copy file from secondary directory to transfer holding directory
                logger.debug(os.path.join(os.path.join(direcSecondary, folder), file))
                logger.debug(os.path.join(direcTransfer, name[1]))
                shutil.copy2(src=os.path.join(os.path.join(direcSecondary, folder), file),
                             dst=os.path.join(direcTransfer, name[1]), follow_symlinks=True)


if __name__ == "__main__":
    app()
