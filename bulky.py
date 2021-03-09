import sys
import os
import shutil
from pathlib import Path

taskProduction = False
taskMoveUp = False

paramVerbose = False
paramDump = False

optFile = False
optDir = False
optRecursive = False
optCapitalize = False
optIgnoreExt = False

paramPath = None
paramKeepLeft = None
paramKeepRight = None
paramReplace = None
paramWith = None
paramInsert = None
paramAt = 0
paramAppend = None
paramStripLeft = None
paramStripRight = None
paramFileAsParent = None

# Return None if empty string
def getVal(strValue,intLength):
    ret = strValue[intLength:]
    if len(ret) == 0:
        ret = None
    return ret

# Exit if None
def ifNoneThenExit(strValue,strMessage):
    if strValue == None:
        print(strMessage)
        sys.exit()
# Exit if not int
def ifNotIntThenExit(strValue,strMessage):
    try:
        int(strValue)
    except ValueError:
        print(strMessage)
        sys.exit()
# Return 1 if defined
def ifDefinedReturnOne(strValue):
    ret = 0
    if strValue != None:
        ret = 1
    return ret

# Return True if defined
def ifDefinedReturnTrue(strValue):
    ret = False
    if strValue != None:
        ret = True
    return ret

# Do actual work here < --------------
def goProcessFileAsParent(lparamPath,lparamFileAsParent,loptCapitalize,ltaskMoveUp,ltaskProduction):
    lCurrentFilePath = ""
    lCurrentFileNameArray = ""
    lNewFilePath = None
    lNewFileName = None
    for itemSubfolder in os.listdir(lparamPath):
        if os.path.isdir(lparamPath + itemSubfolder):
            for itemFile in os.listdir(lparamPath + itemSubfolder):
                if itemFile == lparamFileAsParent:
                    lCurrentFileNameArray = itemFile.rsplit('.', 1)
                    lCurrentFilePath = lparamPath + itemSubfolder + os.sep + itemFile
                    lNewFileName = itemSubfolder + "." + lCurrentFileNameArray[1]
                    lNewFilePath = lparamPath + itemSubfolder + os.sep + itemSubfolder + "." + lCurrentFileNameArray[1]
                    print( lCurrentFilePath + "\t==>\t" + lNewFilePath + "\t==\t", end='')
            if lCurrentFilePath == None or lNewFilePath == None:
                print("No files - " + lparamPath)
            else:
                if ltaskProduction:
                    if not os.path.exists(lNewFilePath):
                        try:
                            os.rename(lCurrentFilePath, lNewFilePath)
                            if taskMoveUp:
                                print ("Done => Moving file up one dir ... ", end='')
                                p = Path(lNewFilePath).absolute()
                                parent = p.parents[1]
                                os.rename(str(p),str(parent) + os.sep + lNewFileName)
                                print ("Done!")
                            else:
                                print ("Done!")
                        except:
                            print("Error executing ")
                    else:
                        print("Duplicate - skipping")
                else:
                    if not os.path.exists(lNewFilePath):
                        if taskMoveUp:
                            print ("Test => Moving file up one dir ... ", end='')
                            print ("Test!")
                        else:
                            print ("Test!")
                    else:
                        print("Duplicate - skipping")

def goProcess(lparamPath,loptRecursive,loptDir,loptFile,loptIgnoreExt,loptCapitalize,lparamKeepLeft,lparamKeepRight,lparamReplace,lparamWith,lparamInsert,lparamAt,lparamAppend,lparamStripLeft,lparamStripRight,lparamFileAsParent,ltaskProduction):
    for subItem in os.listdir(lparamPath):
        paramSubPath = lparamPath + subItem
        if os.path.isdir(paramSubPath):
            if not paramSubPath.endswith(os.sep):
                paramSubPath = paramSubPath + os.sep
            if loptRecursive:
                goProcess(paramSubPath,loptRecursive,loptDir,loptFile,loptIgnoreExt,loptCapitalize,lparamKeepLeft,lparamKeepRight,lparamReplace,lparamWith,lparamInsert,lparamAt,lparamAppend,lparamStripLeft,lparamStripRight,lparamFileAsParent,ltaskProduction)
            if loptDir:
                goProcessEntry(paramSubPath,loptRecursive,loptDir,loptFile,loptIgnoreExt,loptCapitalize,lparamKeepLeft,lparamKeepRight,lparamReplace,lparamWith,lparamInsert,lparamAt,lparamAppend,lparamStripLeft,lparamStripRight,lparamFileAsParent,ltaskProduction)
        if os.path.isfile(paramSubPath):
            if loptFile:
                goProcessEntry(paramSubPath,loptRecursive,loptDir,loptFile,loptIgnoreExt,loptCapitalize,lparamKeepLeft,lparamKeepRight,lparamReplace,lparamWith,lparamInsert,lparamAt,lparamAppend,lparamStripLeft,lparamStripRight,lparamFileAsParent,ltaskProduction)

def goProcessEntry(lparamPath,loptRecursive,loptDir,loptFile,loptIgnoreExt,loptCapitalize,lparamKeepLeft,lparamKeepRight,lparamReplace,lparamWith,lparamInsert,lparamAt,lparamAppend,lparamStripLeft,lparamStripRight,lparamFileAsParent,ltaskProduction):
    if lparamPath[-1] == os.sep: # Remove trailing directory separator if present
        lparamPath = lparamPath[:-1]
    lPathArray = lparamPath.rsplit(os.sep,1) # Split path by directory separator

    p = Path(lparamPath).absolute() # Get path of item
    lPath = str(p.parents[0]) + os.sep
    if loptDir or (loptFile and loptIgnoreExt): # Get name of item + extension if applied
        lOldVal = lPathArray[1]
        lExt = ""
    elif loptFile:
        f = lPathArray[1].rsplit(".",1)
        lOldVal = f[0]
        lExt = "."+f[1]

    if ifDefinedReturnOne(lparamKeepLeft) + ifDefinedReturnOne(lparamKeepRight) > 0:
        lNewVal = ""
        if ifDefinedReturnOne(lparamKeepLeft):
            res = lOldVal[:int(lparamKeepLeft)]
            lNewVal += res
        if ifDefinedReturnOne(lparamKeepRight):
            res = lOldVal[- int(lparamKeepRight):]
            lNewVal += res

    if ifDefinedReturnOne(lparamStripLeft) + ifDefinedReturnOne(lparamStripRight) > 0:
        lNewVal = ""
        if ifDefinedReturnOne(lparamStripLeft):
            res = lOldVal[int(lparamStripLeft):]
            lNewVal += res
        if ifDefinedReturnOne(lparamStripRight):
            res = lOldVal[:-int(lparamStripRight)]
            lNewVal += res

    if ifDefinedReturnOne(lparamInsert) + ifDefinedReturnOne(lparamAppend) > 0:
        lNewVal = ""
        if ifDefinedReturnOne(lparamInsert) and not ifDefinedReturnOne(lparamAppend):
            if lparamAt != 0:
                res = lOldVal[:int(lparamAt)] + lparamInsert + lOldVal[int(lparamAt):]
            else:
                res = lparamInsert + lOldVal
            lNewVal += res
        elif not ifDefinedReturnOne(lparamInsert) and ifDefinedReturnOne(lparamAppend):
            res = lOldVal + lparamAppend
            lNewVal += res
        else:
            if lparamAt != 0:
                res = lOldVal[:int(lparamAt)] + lparamInsert + lOldVal[int(lparamAt):] + lparamAppend
            else:
                res = lparamInsert + lOldVal + lparamAppend
            lNewVal += res
        
    if ifDefinedReturnOne(lparamReplace) + ifDefinedReturnOne(lparamWith) > 0:
        lNewVal = ""
        res = lOldVal.replace(lparamReplace,lparamWith)
        lNewVal += res

    if loptCapitalize:
        lNewVal = lNewVal.title()
    lNewVal += lExt

    print(lparamPath + "\t==>\t" + lPath + lNewVal + "\t==\t", end='')
    
    if ltaskProduction:
        if not os.path.exists(lPath + lNewVal):
            try:
                os.rename(lparamPath, lPath + lNewVal)
                print("Done!")
            except:
                print("Error executing ")
        else:
            print("Duplicate - skipping")
    else:
        print("Test")
    


if len(sys.argv)>1:
    for i in range(len(sys.argv)):
        if sys.argv[i].startswith("--options="):
            if "f" in sys.argv[i][10:]:
                optFile = True
            if "d" in sys.argv[i][10:]:
                optDir = True
            if "r" in sys.argv[i][10:]:
                optRecursive = True
            if "c" in sys.argv[i][10:]:
                optCapitalize = True
            if "i" in sys.argv[i][10:]:
                optIgnoreExt = True
        
        # Path
        if sys.argv[i].startswith("--path="):
            paramPath = getVal(sys.argv[i],7)
            ifNoneThenExit(paramPath,"<path> not defined")
            if not paramPath.endswith(os.sep):
                paramPath = paramPath + os.sep
            if not os.path.exists(paramPath):
                print("Invalid path")
                sys.exit()
            else:
                if not os.path.isdir(paramPath):
                    print("Path is not a directory")
                    sys.exit()

        # Keep left or right n of characters
        if sys.argv[i].startswith("--keep-left="):
            paramKeepLeft = getVal(sys.argv[i],12)
            ifNoneThenExit(paramKeepLeft,"<keep left> not defined")
            ifNotIntThenExit(paramKeepLeft,"Non-int <keep left> value")
        if sys.argv[i].startswith("--keep-right="):
            paramKeepRight = getVal(sys.argv[i],13)
            ifNoneThenExit(paramKeepRight,"<keep right> not defined")
            ifNotIntThenExit(paramKeepRight,"Non-int <keep right> value")

        # Replace this with that
        if sys.argv[i].startswith("--replace="):
            paramReplace = getVal(sys.argv[i],10)
            ifNoneThenExit(paramReplace,"<replace> not defined")
        if sys.argv[i].startswith("--with="):
            paramWith = getVal(sys.argv[i],7)
            ifNoneThenExit(paramWith,"<with> not defined")
            if paramWith == "null": paramWith = ""
            if paramWith == "space": paramWith = " "

        # Insert what where and append at end
        if sys.argv[i].startswith("--insert="):
            paramInsert = getVal(sys.argv[i],9)
            ifNoneThenExit(paramInsert,"<insert> not defined")
        if sys.argv[i].startswith("--at="):
            paramAt = getVal(sys.argv[i],5)
            ifNoneThenExit(paramAt,"<at> not defined")
            ifNotIntThenExit(paramAt,"Non-int <at> value")
        if sys.argv[i].startswith("--append="):
            paramAppend = getVal(sys.argv[i],9)
            ifNoneThenExit(paramAppend,"<append> not defined")

        # Strip from left or right
        if sys.argv[i].startswith("--strip-left="):
            paramStripLeft = getVal(sys.argv[i],13)
            ifNoneThenExit(paramStripLeft,"<strip left> not defined")
            ifNotIntThenExit(paramStripLeft,"Non-int <strip left> value")
        if sys.argv[i].startswith("--strip-right="):
            paramStripRight = getVal(sys.argv[i],14)
            ifNoneThenExit(paramStripRight,"<strip right> not defined")
            ifNotIntThenExit(paramStripRight,"Non-int <strip right> value")

        # Rename file as container folder and move one folder up
        if sys.argv[i].startswith("--file-as-parent="):
            paramFileAsParent = getVal(sys.argv[i],17)
            ifNoneThenExit(paramFileAsParent,"<file-as-parent> search file not defined")
        if sys.argv[i].startswith("--move-up"):
            taskMoveUp = True
        
        # Do anything with files?
        if sys.argv[i] == "--make-it-so":
            taskProduction = True

        if sys.argv[i] == "--verbose":
            paramVerbose = True

        if sys.argv[i] == "--dump":
            paramDump = True

    if paramDump:
        print('taskProduction',taskProduction)
        print('taskMoveUp',taskMoveUp)
        print('optFile',optFile)
        print('optDir',optDir)
        print('optRecursive',optRecursive)
        print('optCapitalize',optCapitalize)
        print('optIgnoreExt',optIgnoreExt)
        print('paramPath',paramPath)
        print('paramKeepLeft',paramKeepLeft)
        print('paramKeepRight',paramKeepRight)
        print('paramReplace',paramReplace)
        print('paramWith',paramWith)
        print('paramInsert',paramInsert)
        print('paramAt',paramAt)
        print('paramAppend',paramAppend)
        print('paramStripLeft',paramStripLeft)
        print('paramStripRight',paramStripRight)
        print('paramFileAsParent',paramFileAsParent)
        print('paramVerbose',paramVerbose)
        print('paramDump',paramDump)
        sys.exit()
        
    if (paramReplace == None or paramWith == None) and paramReplace != paramWith:
        print("<replace> and <with> must both be defined")
        sys.exit()

    ifNoneThenExit(paramPath,"No path specified")
    if (not optFile and not optDir) and not ifDefinedReturnTrue(paramFileAsParent):
        print("Either 'File' or 'Directory' option must be set, od the task must be '--file-as-parent'")
        sys.exit()
    
    if  not ifDefinedReturnTrue(paramFileAsParent) and taskMoveUp:
        print("Task '--move-up' can only be used in combination with '--file-as-parent'")
        sys.exit()

    intKeep = 0
    intStrip = 0
    intInsApp = 0
    intReplace = 0
    intFAP = 0
    if ifDefinedReturnOne(paramKeepLeft) + ifDefinedReturnOne(paramKeepRight) > 0: intKeep = 1
    if ifDefinedReturnOne(paramStripLeft) + ifDefinedReturnOne(paramStripRight) > 0: intStrip = 1
    if ifDefinedReturnOne(paramInsert) + ifDefinedReturnOne(paramAppend) > 0: intInsApp = 1
    if ifDefinedReturnOne(paramReplace) + ifDefinedReturnOne(paramWith) > 0: intReplace = 1
    if ifDefinedReturnOne(paramFileAsParent): intFAP = 1
    if intKeep + intStrip + intInsApp + intReplace + intFAP > 1:
        print("Too many tasks")
        sys.exit()
    elif intKeep + intStrip + intInsApp + intReplace + intFAP == 0:
        print("No task specified")
        sys.exit()

    if taskProduction:
        print("This is a production run")
    else:
        print("This is a test run")

    # If the program survived this long - initialize crawler
    if ifDefinedReturnTrue(paramFileAsParent): 
        goProcessFileAsParent(paramPath,paramFileAsParent,optCapitalize,taskMoveUp,taskProduction)
    else:
        goProcess(paramPath,optRecursive,optDir,optFile,optIgnoreExt,optCapitalize,paramKeepLeft,paramKeepRight,paramReplace,paramWith,paramInsert,paramAt,paramAppend,paramStripLeft,paramStripRight,paramFileAsParent,taskProduction)
else:
    print("Help")
    print("")
    print("\t--options=<options>")
    print("Options:")
    print("\tf\t\t\t\t\tRename files")
    print("\td\t\t\t\t\tRename directories")
    print("\tr\t\t\t\t\tRecursive run")
    print("\tc\t\t\t\t\tCapitalize words - Note: This will capitalize everything in path, regardless of the matching.")
    print("\ti\t\t\t\t\tIgnore extensions (in combination with <f>)")
    print("")
    print("\t--path=<path>")
    print("")
    print("Operations (output is grouped by allowed combinations):")
    print("\t--keep-left=<int>\t\t\tKeep <int> characters on left")
    print("\t--keep-right=<int>\t\t\tKeep <int> characters on right")
    print("")
    print("\t--replace==<str>\t\t\tReplace <str>")
    print("\t--with=<str>\t\t\t\tWith <str>")
    print("\t\tnull => replace with nothing")
    print("\t\tspace => replace with space")
    print("")
    print("\t--insert=<str>\t\t\t\tInsert <str> at start")
    print("\t--at=<int>\t\t\t\tInsert <str> at <int>")
    print("\t--append=<str>\t\t\t\tAppend <str> to end")
    print("")
    print("\t--strip-left=<int>\t\t\tStrip <int> characters from start")
    print("\t--strip-right=<int>\t\t\tStrip <int> characters from end")
    print("")
    print("\t(in combination with -o=d)")
    print("\t--file-as-parent=<search_file_name>\trename <search_file_name> to match parent directory name")
    print("\t--move-up\t\t\t\tMove file un one directory")
    print("")
    print("All operations only output what will happen. To do the actual task, use the production run switch")
    print("\t--make-it-so\t\t\t\tDo a production run")
    print("")
    print("\t--dump\t\t\t\tPrint detected arguments")
    print("\t--verbose\t\t\t\tVerbose output")
    print("")
    print("Example:")
    print("\tbr.py -o=fri --path=/temp/directory --replace=hello --with=world")
    print("\tbr.py -o=fri --path=/temp/directory --keep-left=10 --keep-right=5")
    print("\tbr.py -o=fri --path=/temp/directory --strip-left=5 --strip-right=5")
    print("\tbr.py -o=fri --path=/temp/directory --insert=hello --at=4 --append=world")
    print("\tbr.py -o=d --path=/temp/directory --file-as-parent=file.ext --move-up")