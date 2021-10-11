import glob
import logging
import os
import os.path
import re
import fnmatch

filesLog = logging.getLogger('AndSync.Files')

def dirDiff(direcPrimary, direcSecondary):
    """Compares primary directory to secondary directory and returns a list of all files that differ between the two directoreies"""

    if not os.path.isdir(direcPrimary) or not os.path.isdir(direcSecondary):
        filesLog.warning("One of the directories provided does not exist or current user does not have required permissions to access")
        return
    fstyle = "*"
    filesLog.debug(direcPrimary)
    filesLog.debug(str(os.path.join(direcPrimary, fstyle)))
    filesLog.debug(direcSecondary)
    filesLog.debug(str(os.path.join(direcSecondary, fstyle)))

    primaryFiles = os.path.split(glob.glob(os.path.join(direcPrimary, fstyle)))[1]
    secondaryFiles = os.path.split(glob.glob(os.path.join(direcSecondary, fstyle)))[1]

    diffList = [f for f in primaryFiles if f not in secondaryFiles]

    filesLog.info("Total file difference is %d files" % len(diffList))

    return diffList