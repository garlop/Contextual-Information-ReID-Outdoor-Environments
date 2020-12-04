#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example shows how to use dlib's face recognition tool for clustering using chinese_whispers.
#   This is useful when you have a collection of photographs which you know are linked to
#   a particular person, but the person may be photographed with multiple other people.
#   In this example, we assume the largest cluster will contain photos of the common person in the
#   collection of photographs. Then, we save extracted images of the face in the largest cluster in
#   a 150x150 px format which is suitable for jittering and loading to perform metric learning (as shown
#   in the dnn_metric_learning_on_images_ex.cpp example.
#   https://github.com/davisking/dlib/blob/master/examples/dnn_metric_learning_on_images_ex.cpp
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake installed.  On Ubuntu, this can be done easily by running the
#   command:
#       sudo apt-get install cmake
#
#   Also note that this example requires Numpy which can be installed
#   via the command:
#       pip install numpy

import sys
import os
import dlib
import numpy as np
import shutil
  
if len(sys.argv) != 3:
    print(
        "Call this program like this:\n"
        "   ./GenerateClusters.py ./descriptors.txt output_folder")
    exit()

descriptor_file_path = sys.argv[1]
output_folder_path = sys.argv[2]

descriptors = []
images = []

# Now find all the persons 1024D descriptors.

personDesc = open(descriptor_file_path, "r") 

for line in personDesc:
    descriptorElements = line.split("|")
    print("Processing image: {}".format(descriptorElements[0]))

    # Compute the 128D vector that describes the face in img identified by
    # shape.
    descriptor = np.array(descriptorElements[1:])
    descriptor = descriptor.astype(np.float) 
    descriptors.append(dlib.vector(descriptor))
    images.append(descriptorElements[0])

#descriptors = dlib.vector(descriptors)

# Now let's cluster the faces.  
labels = dlib.chinese_whispers_clustering(descriptors, 0.20)
num_classes = len(set(labels))
print("Number of clusters: {}".format(num_classes))

# Find biggest class
biggest_class = None
biggest_class_length = 0
for i in range(0, num_classes):
    class_length = len([label for label in labels if label == i])
    if class_length > biggest_class_length:
        biggest_class_length = class_length
        biggest_class = i

print("Biggest cluster id number: {}".format(biggest_class))
print("Number of persons in biggest cluster: {}".format(biggest_class_length))

# Find the indices for the biggest class
indices = []
for i, label in enumerate(labels):
    if label == biggest_class:
        indices.append(i)

print("Indices of images in the biggest cluster: {}".format(str(indices)))

# Save the extracted faces
print("Saving persons in every cluster to output folder...")
for i, label in enumerate(labels):
    img = images[i]
 # Ensure output directory exists
    if not os.path.isdir(output_folder_path+"/"+str(label)):
        os.makedirs(output_folder_path+"/"+str(label))
    shutil.copy("../../3Unlabeled Data/output/"+str(img), output_folder_path+str(label))
