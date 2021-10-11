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

    primaryFiles = glob.glob(os.path.join(direcPrimary, fstyle))
    secondaryFiles = glob.glob(os.path.join(direcSecondary, fstyle))

    primaryFnames = []
    secondaryFnames = []
    for file in primaryFiles:
        primaryFnames.append(os.path.split(file)[1])
    for file in secondaryFiles:
        secondaryFnames.append(os.path.split(file)[1])


    #diffList = [f for f in primaryFnames if f not in secondaryFnames]
    diffList = [f for f in primaryFiles if os.path.split(f)[1] not in secondaryFnames]

    for i in range(5):
        print(diffList[i])

    filesLog.info("Total file difference is %d files" % len(diffList))

    return diffList

def locateFile(direcStart, maxDepth, fname):
    """Searches for the given filename starting in the given start directory and recursively scanning to the specified depth.
    Returns None if the the cannot be found within the given parameters"""

    fileList = []

    for depth in range(1, maxDepth + 1):
        if depth == 1:
            maxGlob = fname
        else:
            maxGlob = ("*/" * (depth - 1) +fname)

        filesLog.info(maxGlob)

        searchDir = os.path.join(direcStart, maxGlob)
        filesLog.info(searchDir)

        allFiles = glob.glob(searchDir)
        fileList.extend(file for file in allFiles if (os.path.split(file)[1] == fname and file != os.path.join(direcStart, fname)))

        filesLog.info("Found filename in %d other location(s)" % len(fileList))
        
    return