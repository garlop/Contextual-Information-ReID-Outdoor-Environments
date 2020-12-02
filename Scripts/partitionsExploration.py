import pickle
import requests
import json
import os
from random import randint
import numpy as np

#THIS PART WAS TO ASSIGN A 10% OF THE IMAGES RANDOMLY AS QUERY IMAGES
f = open("imagesprinted.txt", "r")

files = []
numbers = []
while True:
    line = f.readline()
    if len(line) == 0: break
    files.append(line.rstrip())
    numbers.append(np.random.choice(np.arange(0, 2), p=[0.1, 0.9]))

partitions = { 'test_im_names' : files, 
#'test_marks' : numbers}

#pickling_on = open("filesNames.pkl","w")
#pickle.dump(partitions, pickling_on)
#pickling_on.close()

#with open('filesNames.pkl', 'rb') as f:
#    partitions = pickle.load(f)
#    print(partitions)
#f.close()

#THIS PART OF THE CODE WAS TO OVERRIDE ERRORS ON IMAGES ALREADY SALVED.
#with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'rb') as f:
#    partitions = pickle.load(f)
#    im_names = partitions['{}_im_names'.format('test')]
#    marks = partitions['test_marks']
#    print(im_names.index('V222858_p00003.png'))
#    #print(im_names.index("V223802_p00001.png"))
#    #print(im_names.index("V223814_p00001.png"))
#    #print(im_names.index("V223775_p00001.png"))
#    #print(im_names.index("V223789_p00001.png"))
#    #print(marks[im_names.index("V223802_p00001.png")])
#    new_im_names = im_names[:]
#    new_im_names[im_names.index('V222858_p00003.png')] = "V222858_p1.png"
#
#    partitions['{}_im_names'.format('test')] = new_im_names
#f.close()

#with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'w') as f:
#    pickle.dump(partitions, f)
#f.close()

#THIS PART IS TO ANALYSE HOW IS THE ADVANCEMENT IN THE LABELING TASK GOING SO FAR.
with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'rb') as f:
    partitions = pickle.load(f)
    im_names = partitions['{}_im_names'.format('test')]


    notlabeled = 0
    labeled = 0
    for im_name in im_names:
        if len(im_name) > 15:
            labeled = labeled + 1
        else:
            notlabeled = notlabeled + 1

    advancementpercent = (float(labeled)/(labeled+notlabeled))*100
    print(labeled)
    print(notlabeled)
    print("total advance so far is: "+str(advancementpercent)+"%")

f.close()
