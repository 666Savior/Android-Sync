import glob
import hashlib
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

    filesLog.info("Total file difference is %d files" % len(diffList))

    return diffList


def dirFolderScan(direc):

    if not os.path.isdir(direc):
        filesLog.warning("Directory provided does not exist or current user does not have permission to access")

    folders = glob.glob(f'{direc}/*/**/', recursive=True)
    filesLog.debug(folders)

    return folders

def dirSync(direcPrimary, direcSecondary, destructive=False):
    """Adjusts secondary directory to contain the same folders as primary directory. If destructive is true,
    deletes any folders in the secondary directory that do no exist in the primary directory"""

    primaryTmp = dirFolderScan(direcPrimary)
    primary = []
    for path in primaryTmp:
        primary.append(re.sub(direcPrimary.rstrip("/"), '', path))
    filesLog.debug(primary)

    secondaryTmp = dirFolderScan(direcSecondary)
    secondary = []
    for path in secondaryTmp:
        secondary.append(re.sub(direcSecondary.rstrip("/"), '', path))
    filesLog.debug(secondary)

    diff = [f for f in primary if f not in secondary]
    print(diff)

    print(direcPrimary)
    print(direcSecondary.rstrip("/"))
    for path in diff:

        path = path.replace("\\", "/").lstrip("/")

        print(path)
        print(os.path.join(direcSecondary, path))

        if not os.path.isdir(os.path.join(direcSecondary, path)):
            os.makedirs(os.path.join(direcSecondary, path))

    if destructive:
        diffDestroy = [f for f in secondary if f not in primary]
        print(diffDestroy)

    return

def locateFile(direcStart, maxDepth, fname, direcSkip=None):
    """Searches for the given filename starting in the given start directory and recursively scanning to the specified depth.
    Returns None if the file cannot be found within the given parameters."""

    fileList = []

    for depth in range(1, maxDepth + 1):
        if depth == 1:
            maxGlob = fname
        else:
            maxGlob = ("*/" * (depth - 1) + fname)

        searchDir = os.path.join(direcStart, maxGlob)
        filesLog.debug(searchDir)

        allFiles = glob.glob(searchDir)
        fileList.extend([file for file in allFiles if os.path.split(file)[1] == fname]) #and file != os.path.join("D:/~Dropbox/Dropbox/Pictures/General/Art\\Moe - Phone Copy\\", fname))])

    filesLog.debug(fname)
    filesLog.debug("Found filename in %d other location(s)" % len(fileList))

    for file in fileList:
        filesLog.debug(file)

    return fileList


def isDuplicate(primaryFile, secondaryFile):

    if not os.path.isfile(primaryFile) or not os.path.isfile(secondaryFile):
        filesLog.warning("One of the provided filenames does not exist or the current user does not have permissions to access")

    with open(primaryFile, 'rb') as primary:
        primaryHash = hashlib.sha512(primary.read()).hexdigest()
    with open(secondaryFile, 'rb') as secondary:
        secondaryHash = hashlib.sha512(secondary.read()).hexdigest()

    filesLog.info("First file's hash: %s" % primaryHash)
    filesLog.info("Second file's hash: %s" % secondaryHash)

    if primaryHash == secondaryHash:
        filesLog.info("File hashes match, files are duplicate")
        return True
    else:
        filesLog.info("File hashes do not match")
        return False
