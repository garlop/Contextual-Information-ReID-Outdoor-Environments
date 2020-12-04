from os import listdir
from os.path import isfile, join
import re
import shutil
import os

folder = '../../5Labeled Data/labeledNewFolders/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

sourcePath = r'../../5Labeled Data/labeledNew/'
onlyfiles = [f for f in listdir(sourcePath) if isfile(join(sourcePath, f))]

for file in onlyfiles:
    result = re.search(r'_p\d*',file)
    id = result.group()[2:]

    destinationPath = r'../../5Labeled Data/labeledNewFolders/'+id

    if not os.path.exists(destinationPath):
        os.makedirs(destinationPath)

    srcpath = os.path.join(sourcePath, file)
    dstpath = os.path.join(destinationPath, file)
    shutil.copyfile(srcpath, dstpath)


onlyfolders = [fold for fold in listdir(folder) if not isfile(join(folder, fold))]

test_folders = onlyfolders[int(len(onlyfolders)*.8):]
train_folders = onlyfolders[:int(len(onlyfolders)*.8)]

trainfolder = r'../../5Labeled Data/labeledNewFolders/bounding_box_train/'
testfolder = r'../../5Labeled Data/labeledNewFolders/bounding_box_test/'

queryfolder = r'../../5Labeled Data/labeledNewFolders/query/'

if not os.path.exists(trainfolder):
    os.makedirs(trainfolder)

if not os.path.exists(testfolder):
    os.makedirs(testfolder)

if not os.path.exists(queryfolder):
    os.makedirs(queryfolder)

for fold in onlyfolders:
    if fold in train_folders:
        shutil.copytree(folder+fold, trainfolder+fold)
    else:
        shutil.copytree(folder+fold, testfolder+fold)
    shutil.copytree(folder+fold, queryfolder+fold)
    shutil.rmtree(folder+fold)
