from os import listdir
from os.path import isfile, join
import sys
import re
import shutil
import os

if len(sys.argv) != 3:
    print(
        "Call this program like this:\n"
        "   ./PhotosUnionAndRenaming.py 1(InitialFolder) 503(FinalFolder)")
    exit()

initialFolder = int(sys.argv[1])
finalFolder = int(sys.argv[2])

currentFolder = initialFolder

##First we need to make sure the folder is empty
try:
    shutil.rmtree('../../5Labeled Data/labeledNew/')
except:
    print("the folder was not there, maybe it is the first time this program runs")
os.mkdir('../../5Labeled Data/labeledNew/')

while (currentFolder <= finalFolder):
    try:
        onlyfiles = [f for f in listdir("../../5Labeled Data/Clases/"+str(currentFolder)) if isfile(join("../../5Labeled Data/Clases/"+str(currentFolder), f))]
        modifiedStrings = [re.sub("_p[0-9]*.", "_p"+str(currentFolder)+".",newLabeledString) for newLabeledString in onlyfiles ]
        i=0
        for newfile in modifiedStrings:
            shutil.copy("../../5Labeled Data/Clases/"+str(currentFolder)+"/"+onlyfiles[i], '.../../5Labeled Data/labeledNew/'+newfile)
            i=i+1
    except:
        print("folder dont exist, maybe moved complete")
    currentFolder = currentFolder + 1
