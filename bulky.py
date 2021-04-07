import sys
import os
import shutil
from pathlib import Path
import re
from copy import copy, deepcopy


class startup:
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
    paramRegex = False
    paramRegexIgnoreCase = False

    paramInsert = None
    paramAt = 0
    paramAppend = None

    paramStripLeft = None
    paramStripRight = None

    paramMatch = None
    paramNoMatch = None

    paramFileAsParent = None

s = startup()

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
#def goProcessFileAsParent(lparamPath,lparamFileAsParent,loptCapitalize,ltaskMoveUp,ltaskProduction):
def goProcessFileAsParent(ls):
    lCurrentFilePath = ""
    lCurrentFileNameArray = ""
    lNewFilePath = None
    lNewFileName = None
    for itemSubfolder in os.listdir(ls.paramPath):
        if os.path.isdir(ls.paramPath + itemSubfolder):
            for itemFile in os.listdir(ls.paramPath + itemSubfolder):
                if itemFile == ls.paramFileAsParent:
                    lCurrentFileNameArray = itemFile.rsplit('.', 1)
                    lCurrentFilePath = ls.paramPath + itemSubfolder + os.sep + itemFile
                    lNewFileName = itemSubfolder + "." + lCurrentFileNameArray[1]
                    lNewFilePath = ls.paramPath + itemSubfolder + os.sep + itemSubfolder + "." + lCurrentFileNameArray[1]
                    print( lCurrentFilePath + "\t==>\t" + lNewFilePath + "\t==\t", end='')
            if lCurrentFilePath == None or lNewFilePath == None:
                print("No files - " + ls.paramPath)
            else:
                if ls.taskProduction:
                    if not os.path.exists(lNewFilePath):
                        try:
                            os.rename(lCurrentFilePath, lNewFilePath)
                            if ls.taskMoveUp:
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
                        if ls.taskMoveUp:
                            print ("Test => Moving file up one dir ... ", end='')
                            print ("Test!")
                        else:
                            print ("Test!")
                    else:
                        print("Duplicate - skipping")

def goProcess(ls):
    for subItem in os.listdir(ls.paramPath):
        paramSubPath = ls.paramPath + subItem
        if os.path.isdir(paramSubPath):
            if not paramSubPath.endswith(os.sep):
                paramSubPath = paramSubPath + os.sep
            ls1 = copy(ls)
            ls1.paramPath = paramSubPath
            if ls.optRecursive:
                goProcess(ls1)
            if ls.optDir:
                goProcessEntry(ls1)
        if os.path.isfile(paramSubPath):
            ls1 = copy(ls)
            ls1.paramPath = paramSubPath
            if ls.optFile:
                goProcessEntry(ls1)

def goProcessEntry(ls):
    if ls.paramPath[-1] == os.sep: # Remove trailing directory separator if present
        ls.paramPath = ls.paramPath[:-1]
    lPathArray = ls.paramPath.rsplit(os.sep,1) # Split path by directory separator

    p = Path(ls.paramPath).absolute() # Get path of item
    lPath = str(p.parents[0]) + os.sep
    if ls.optDir or (ls.optFile and ls.optIgnoreExt): # Get name of item + extension if applied
        lOldVal = lPathArray[1]
        lExt = ""
    elif ls.optFile:
        f = lPathArray[1].rsplit(".",1)
        lOldVal = f[0]
        lExt = "."+f[1]

    if (ifDefinedReturnTrue(ls.paramMatch) and ls.paramPath.find(ls.paramMatch) > -1) or (not ifDefinedReturnTrue(ls.paramMatch) and not ifDefinedReturnTrue(ls.paramNoMatch)) or (ifDefinedReturnTrue(ls.paramNoMatch) and ls.paramPath.find(ls.paramNoMatch) == -1): # Run if MATCH defined and true, or when not defined, or when NOMATCH 
        if ifDefinedReturnOne(ls.paramKeepLeft) + ifDefinedReturnOne(ls.paramKeepRight) > 0:
            lNewVal = ""
            if ifDefinedReturnOne(ls.paramKeepLeft):
                res = lOldVal[:int(ls.paramKeepLeft)]
                lNewVal += res
            if ifDefinedReturnOne(ls.paramKeepRight):
                res = lOldVal[- int(ls.paramKeepRight):]
                lNewVal += res

        if ifDefinedReturnOne(ls.paramStripLeft) + ifDefinedReturnOne(ls.paramStripRight) > 0:
            lNewVal = ""
            if ifDefinedReturnOne(ls.paramStripLeft):
                res = lOldVal[int(ls.paramStripLeft):]
                lNewVal += res
            if ifDefinedReturnOne(ls.paramStripRight):
                res = lOldVal[:-int(ls.paramStripRight)]
                lNewVal += res

        if ifDefinedReturnOne(ls.paramInsert) + ifDefinedReturnOne(ls.paramAppend) > 0:
            lNewVal = ""
            if ifDefinedReturnOne(ls.paramInsert) and not ifDefinedReturnOne(ls.paramAppend):
                if ls.paramAt != 0:
                    res = lOldVal[:int(ls.paramAt)] + ls.paramInsert + lOldVal[int(ls.paramAt):]
                else:
                    res = ls.paramInsert + lOldVal
                lNewVal += res
            elif not ifDefinedReturnOne(ls.paramInsert) and ifDefinedReturnOne(ls.paramAppend):
                res = lOldVal + ls.paramAppend
                lNewVal += res
            else:
                if ls.paramAt != 0:
                    res = lOldVal[:int(ls.paramAt)] + lparamInsert + lOldVal[int(ls.paramAt):] + ls.paramAppend
                else:
                    res = ls.paramInsert + lOldVal + ls.paramAppend
                lNewVal += res
            
        if ifDefinedReturnOne(ls.paramReplace) + ifDefinedReturnOne(ls.paramWith) > 0:
            lNewVal = ""
            if ls.paramRegex:
                if ls.paramRegexIgnoreCase:
                    pattern = re.compile(ls.paramReplace,re.IGNORECASE)
                else:
                    pattern = re.compile(ls.paramReplace)
                res = pattern.sub(ls.paramWith,lOldVal)
            else:
                res = lOldVal.replace(ls.paramReplace,ls.paramWith)
            lNewVal += res

        if ls.optCapitalize:
            lNewVal = lNewVal.title()
        lNewVal += lExt

        print(ls.paramPath + "\t==>\t" + lPath + lNewVal + "\t==\t", end='')
        
        if ls.taskProduction:
            if not os.path.exists(lPath + lNewVal):
                try:
                    os.rename(ls.paramPath, lPath + lNewVal)
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
                s.optFile = True
            if "d" in sys.argv[i][10:]:
                s.optDir = True
            if "r" in sys.argv[i][10:]:
                s.optRecursive = True
            if "c" in sys.argv[i][10:]:
                s.optCapitalize = True
            if "i" in sys.argv[i][10:]:
                s.optIgnoreExt = True
        
        # Path
        if sys.argv[i].startswith("--path="):
            s.paramPath = getVal(sys.argv[i],7)
            ifNoneThenExit(s.paramPath,"<path> not defined")
            if not s.paramPath.endswith(os.sep):
                s.paramPath = s.paramPath + os.sep
            if not os.path.exists(s.paramPath):
                print("Invalid path")
                sys.exit()
            else:
                if not os.path.isdir(s.paramPath):
                    print("Path is not a directory")
                    sys.exit()

        # Keep left or right n of characters
        if sys.argv[i].startswith("--keep-left="):
            s.paramKeepLeft = getVal(sys.argv[i],12)
            ifNoneThenExit(s.paramKeepLeft,"<keep left> not defined")
            ifNotIntThenExit(s.paramKeepLeft,"Non-int <keep left> value")
        if sys.argv[i].startswith("--keep-right="):
            s.paramKeepRight = getVal(sys.argv[i],13)
            ifNoneThenExit(s.paramKeepRight,"<keep right> not defined")
            ifNotIntThenExit(s.paramKeepRight,"Non-int <keep right> value")

        # Replace this with that
        if sys.argv[i].startswith("--replace="):
            s.paramReplace = getVal(sys.argv[i],10)
            ifNoneThenExit(s.paramReplace,"<replace> not defined")
        if sys.argv[i].startswith("--with="):
            s.paramWith = getVal(sys.argv[i],7)
            ifNoneThenExit(s.paramWith,"<with> not defined")
            if s.paramWith == "null": s.paramWith = ""
            if s.paramWith == "space": s.paramWith = " "

        # Insert what where and append at end
        if sys.argv[i].startswith("--insert="):
            s.paramInsert = getVal(sys.argv[i],9)
            ifNoneThenExit(s.paramInsert,"<insert> not defined")
        if sys.argv[i].startswith("--at="):
            s.paramAt = getVal(sys.argv[i],5)
            ifNoneThenExit(s.paramAt,"<at> not defined")
            ifNotIntThenExit(s.paramAt,"Non-int <at> value")
        if sys.argv[i].startswith("--append="):
            s.paramAppend = getVal(sys.argv[i],9)
            ifNoneThenExit(s.paramAppend,"<append> not defined")

        # Strip from left or right
        if sys.argv[i].startswith("--strip-left="):
            s.paramStripLeft = getVal(sys.argv[i],13)
            ifNoneThenExit(s.paramStripLeft,"<strip left> not defined")
            ifNotIntThenExit(s.paramStripLeft,"Non-int <strip left> value")
        if sys.argv[i].startswith("--strip-right="):
            s.paramStripRight = getVal(sys.argv[i],14)
            ifNoneThenExit(s.paramStripRight,"<strip right> not defined")
            ifNotIntThenExit(s.paramStripRight,"Non-int <strip right> value")

        # Rename file as container folder and move one folder up
        if sys.argv[i].startswith("--file-as-parent="):
            s.paramFileAsParent = getVal(sys.argv[i],17)
            ifNoneThenExit(s.paramFileAsParent,"<file-as-parent> search file not defined")
        if sys.argv[i].startswith("--move-up"):
            s.taskMoveUp = True

        if sys.argv[i].startswith("--match="):
            s.paramMatch = getVal(sys.argv[i],8)

        if sys.argv[i].startswith("--no-match="):
            s.paramNoMatch = getVal(sys.argv[i],11)
            
        if sys.argv[i].startswith("--ignore-case"):
            s.paramRegexIgnoreCase = True

        # Do anything with files?
        if sys.argv[i] == "--make-it-so":
            s.taskProduction = True

        if sys.argv[i] == "--verbose":
            s.paramVerbose = True

        if sys.argv[i] == "--regex":
            s.paramRegex = True

        if sys.argv[i] == "--dump":
            s.paramDump = True

    if s.paramDump:
        print('taskProduction\t\t=\t',s.taskProduction)
        print('taskMoveUp\t\t=\t',s.taskMoveUp)
        print('optFile\t\t\t=\t',s.optFile)
        print('optDir\t\t\t=\t',s.optDir)
        print('optRecursive\t\t=\t',s.optRecursive)
        print('optCapitalize\t\t=\t',s.optCapitalize)
        print('optIgnoreExt\t\t=\t',s.optIgnoreExt)
        print('paramPath\t\t=\t',s.paramPath)
        print('paramKeepLeft\t\t=\t',s.paramKeepLeft)
        print('paramKeepRight\t\t=\t',s.paramKeepRight)
        print('paramReplace\t\t=\t',s.paramReplace)
        print('paramWith\t\t=\t',s.paramWith)
        print('paramInsert\t\t=\t',s.paramInsert)
        print('paramAt\t\t\t=\t',s.paramAt)
        print('paramAppend\t\t=\t',s.paramAppend)
        print('paramStripLeft\t\t=\t',s.paramStripLeft)
        print('paramStripRight\t\t=\t',s.paramStripRight)
        print('paramFileAsParent\t=\t',s.paramFileAsParent)
        print('paramVerbose\t\t=\t',s.paramVerbose)
        print('paramDump\t\t=\t',s.paramDump)
        print('paramMatch\t\t=\t',s.paramMatch)
        print('paramNoMatch\t\t=\t',s.paramNoMatch)
        print('paramRegex\t\t=\t',s.paramRegex)
        sys.exit()
        
    if (s.paramReplace == None or s.paramWith == None) and s.paramReplace != s.paramWith:
        print("<replace> and <with> must both be defined")
        sys.exit()

    ifNoneThenExit(s.paramPath,"No path specified")
    if (not s.optFile and not s.optDir) and not ifDefinedReturnTrue(s.paramFileAsParent):
        print("Either 'File' or 'Directory' option must be set, od the task must be '--file-as-parent'")
        sys.exit()
    
    if  not ifDefinedReturnTrue(s.paramFileAsParent) and s.taskMoveUp:
        print("Task '--move-up' can only be used in combination with '--file-as-parent'")
        sys.exit()

    intKeep = 0
    intStrip = 0
    intInsApp = 0
    intReplace = 0
    intFAP = 0
    if ifDefinedReturnOne(s.paramKeepLeft) + ifDefinedReturnOne(s.paramKeepRight) > 0: intKeep = 1
    if ifDefinedReturnOne(s.paramStripLeft) + ifDefinedReturnOne(s.paramStripRight) > 0: intStrip = 1
    if ifDefinedReturnOne(s.paramInsert) + ifDefinedReturnOne(s.paramAppend) > 0: intInsApp = 1
    if ifDefinedReturnOne(s.paramReplace) + ifDefinedReturnOne(s.paramWith) > 0: intReplace = 1
    if ifDefinedReturnOne(s.paramFileAsParent): intFAP = 1
    if ifDefinedReturnOne(s.paramMatch) + ifDefinedReturnOne(s.paramNoMatch) > 1:
        print("--match and --no-match cannot be used together")
        sys.exit()
    if intKeep + intStrip + intInsApp + intReplace + intFAP > 1:
        print("Too many tasks")
        sys.exit()
    elif intKeep + intStrip + intInsApp + intReplace + intFAP == 0:
        print("No task specified")
        sys.exit()

    if s.taskProduction:
        print("This is a production run")
    else:
        print("This is a test run")

    # If the program survived this long - initialize crawler
    if ifDefinedReturnTrue(s.paramFileAsParent): 
        goProcessFileAsParent(s)
        #goProcessFileAsParent(paramPath,paramFileAsParent,optCapitalize,taskMoveUp,taskProduction)
    else:
        goProcess(s)
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
    print("\t--path=<str>")
    print("")
    print("Matching (only one may be used)\tignored when used with --file-as-parent")
    print("\t--match=<str>\t\t\t\tOnly process files containing <str> (including extension)")
    print("\t--no-match=<str>\t\t\t\tOnly process files not containing <str> (including extension)")
    print("")
    print("Operations (output is grouped by allowed combinations):")
    print("\t--keep-left=<int>\t\t\tKeep <int> characters on left")
    print("\t--keep-right=<int>\t\t\tKeep <int> characters on right")
    print("")
    print("\t--replace=<str>\t\t\t\tReplace <str>")
    print("\t--with=<str>\t\t\t\tWith <str>")
    print("\t\tnull => replace with nothing")
    print("\t\tspace => replace with space")
    print("\t--regex\t\t\t\t\tWill assume --replace <str> is regular expression")
    print("\t--ignore-case\t\t\t\t\tWill ignore case of regular expression")
    print("")
    print("\t--insert=<str>\t\t\t\tInsert <str> at start")
    print("\t--at=<int>\t\t\t\tInsert <str> at <int>")
    print("\t--append=<str>\t\t\t\tAppend <str> to end")
    print("")
    print("\t--strip-left=<int>\t\t\tStrip <int> characters from start")
    print("\t--strip-right=<int>\t\t\tStrip <int> characters from end")
    print("")
    print("\t--file-as-parent=<str>\tRename <str> to match parent directory name")
    print("\t--move-up\t\t\t\tMove file up one directory")
    print("")
    print("By default, only task output is displayed - no work is done. To perform the actual task, use the production run switch")
    print("\t--make-it-so\t\t\t\tDo a production run")
    print("")
    print("\t--dump\t\t\t\t\tPrint detected arguments")
    print("\t--verbose\t\t\t\tVerbose output")
    print("")
    print("Example:")
    print("\tbulky.py --options=fdi --path=/temp/directory --replace=hello --with=world")
    print("\tbulky.py --options=fr --path=/temp/directory --keep-left=10 --keep-right=5")
    print("\tbulky.py --options=fc --path=/temp/directory --strip-left=5 --strip-right=5")
    print("\tbulky.py --options=f --path=/temp/directory --insert=hello --at=4 --append=world")
    print("\tbulky.py --path=/temp/directory --file-as-parent=file.ext --move-up")
