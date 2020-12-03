import csv
import json
import numpy as np
from json.decoder import JSONDecodeError

currentData = {'images' : []}
imagesKnown = set()

dataFeaturesFile = "dataMGNFeatures.json"
csvData = "MGNFeatures.csv"

with open(dataFeaturesFile) as json_file:
    try:
        currentData = json.load(json_file)
        for image in currentData["images"]:
            imagesKnown.add(image["imageName"])
    except JSONDecodeError:
        pass

#all_feat = []

with open(csvData, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        keys = ['feat'+str(i) for i in range(2048)]
        features = [row.get(key) for key in keys]
	#all_feat.append(features)
        if(row["imageName"] in imagesKnown):
            print("image", row["imageName"], "already exists")
            pass
        else:
            currentData['images'].append({
                'imageName' : row["imageName"],
                'features' : features
            })
        if (i+1) % 100 == 0:
            print('{} images saved'.format(i))
        i = i+1
#    all_feat = np.concatenate(all_feat)
#    print('all_feat.shape:', all_feat.shape)
#    all_feat = normalize(all_feat, axis=1)

with open(dataFeaturesFile, 'w') as outfile:
    json.dump(currentData, outfile)
