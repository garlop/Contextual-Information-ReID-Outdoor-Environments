import os
import pickle
import numpy as np

entries = os.listdir('./labeledNew/')

files = []
numbers = []

for entry in entries:
    files.append(entry.rstrip())
    numbers.append(0)

partitions = { 'test_im_names' : files, 
'test_marks' : numbers}

pickling_on = open("filesNames.pkl","wb")
pickle.dump(partitions, pickling_on, protocol=2)
pickling_on.close()

with open('filesNames.pkl', 'rb') as f:
    partitions = pickle.load(f)
    print(partitions)
f.close()
