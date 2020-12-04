import csv
import json
import re
import sys
from collections import defaultdict
import datetime

def datetime_to_float(date):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (date - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def searchImageMetaData(imageName, dictionary):
    imageName = "/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/labeledNew/"+imageName
    Lat = dictionary[imageName][0]
    Long = dictionary[imageName][1]
    Feat = dictionary[imageName][2]
    Time = dictionary[imageName][3]
    preInt = dictionary[imageName][4]
    temp = dictionary[imageName][5]
    hum = dictionary[imageName][6]
    press = dictionary[imageName][7]
    WindS = dictionary[imageName][8]
    WindG = dictionary[imageName][9]
    CloudC = dictionary[imageName][10]
    Visb = dictionary[imageName][11]
    return Lat, Long, Feat, Time, preInt, temp, hum, press, WindS, WindG, CloudC, Visb

with open('rankedImages.json', 'r') as response_json:
    imagesRanked = {}
    imagesRanked = json.loads(str(response_json.read()))

dictionary = defaultdict(list)
isEmptyField = False

with open('dataFeatures.json', 'r') as imagesFeatures:
    data = json.load(imagesFeatures)
    images = data['images']
    count = 0
    for attrs in images:
        imageName = attrs["imageName"]
        Lat = attrs["latitude"]
        Long = attrs["longitude"]
        Feat = attrs["features"]
        Time = attrs["time"]
        Time2 = datetime.datetime.strptime(Time, '%Y-%m-%dT%H:%M:%S')
        Time = datetime_to_float(Time2)
        preInt = attrs["precipIntensity"]
        temp = attrs["temperature"]
        hum = attrs["humidity"]
        press = attrs["pressure"]
        WindS = attrs["windSpeed"]
        WindG = attrs["windGust"]
        CloudC = attrs["cloudCover"]
        Visb = attrs["visibility"]
        count = count + 1
        if(temp == ""):
            print("is empty of climate data")
        print("loading data of image:"+imageName+" image "+str(count)+" of "+str(len(images)))
        dictionary[imageName].append(Lat)
        dictionary[imageName].append(Long)
        dictionary[imageName].append(Feat)
        dictionary[imageName].append(Time)
        dictionary[imageName].append(preInt)
        dictionary[imageName].append(temp)
        dictionary[imageName].append(hum)
        dictionary[imageName].append(press)
        dictionary[imageName].append(WindS)
        dictionary[imageName].append(WindG)
        dictionary[imageName].append(CloudC)
        dictionary[imageName].append(Visb)

count = 0

qIFeatHeaders=[]
rIFeatHeaders=[]
for i in range(0,2048):
    print(i)
    qIFeatHeaders.append("qIFeat"+str(i))
    rIFeatHeaders.append("rIFeat"+str(i))


with open('data.csv', 'a+', newline='') as csvData:
    writer = csv.writer(csvData, delimiter='|')
    headers = ['qIC', 'qILat', 'qILong']
    headers.extend(feat for feat in qIFeatHeaders)
    headers.extend(['qITime', 'qIpreInt', 'qItemp', 'qIhum', 'qIpress', 'qIWindS', 'qIWindG', 'qICloudC', 'qIVisb', 'eucDist', 'rIC', 'rILat', 'rILong'])
    headers.extend([feat for feat in rIFeatHeaders])
    headers.extend(['rITime', 'rIpreInt', 'rItemp', 'rIhum', 'qIpress', 'qIwindS', 'qIWindG', 'qICloudC', 'qIVisib', 'areSame'])
    headers.extend(['qI', 'rI', 'ranking'])
    writer.writerow(headers)
    print(headers)  
csvData.close()

for qimage in imagesRanked:
    queryImage = qimage["queryImage"]
    m = re.search('_p[0-9]*',queryImage)
    qIId = m.group(0)[2:]
    qIC = queryImage[1]
    count = count + 1
    print("saving data of image:"+queryImage+" image "+str(count)+" of "+str(len(imagesRanked)))
    qILat, qILong, qIFeat, qITime, qIpreInt, qItemp, qIhum, qIpress, qIWindS, qIWindG, qICloudC, qIVisb = searchImageMetaData(queryImage, dictionary)
    for image in qimage["images"]:
        eucDist = image["distance"]
        n = re.search('_p[0-9]*', image["rankedImage"])
        rIId = n.group(0)[2:]
        rIC = queryImage[1]
        if qIId == rIId:
            areSame = 1
        else:
            areSame = 0
        rILat, rILong, rIFeat, rITime, rIpreInt, rItemp, rIhum, rIpress, rIWindS, rIWindG, rICloudC, rIVisb = searchImageMetaData(image["rankedImage"], dictionary)
        with open('data.csv', 'a+', newline='') as csvData:
            if qItemp == "" or rItemp == "":
                print("row Empty, not saving")
            else:
                writer = csv.writer(csvData, delimiter='|')
                values = [qIC, qILat, qILong]
                values.extend(feat for feat in qIFeat)
                values.extend([qITime, qIpreInt, qItemp, qIhum, qIpress, qIWindS, qIWindG, qICloudC, qIVisb, eucDist, rIC, rILat, rILong])
                values.extend(feat for feat in rIFeat)
                values.extend([rITime, rIpreInt, rItemp, rIhum, rIpress, rIWindS, rIWindG, rICloudC, rIVisb, areSame])
                values.extend([qimage["queryImage"], image["rankedImage"], image["ranking"]])
                writer.writerow(values)

csvData.close()  

#{
#	 'images' : [{
#        'camera' : (int) 1, 2 or 3
#        'imageName' : 'VCXXXXXX_pI.png',
#        'features' : [ARRAY WITH 2048 features each],
#        'latitude' : (float) latitude,
#        'longitude' : (float) longitude,
#        'time' : (string) date and time of picture,
#        'precipIntensity' : value of raining intensity in that moment,
#        'temperature' : value of temperature in that moment,
#        'humidity' : value of humidity in that moment,
#        'pressure' : value of pressure in that moment,
#        'windSpeed' : value of wind Speed in that moment,
#        'windGust' : value of wind Gust in that moment,
#        'cloudCover' : tells if clouds were covering the area,
#        'visibility' : visibility range
#        }]
#}

##    [{
##        "images": [
##            {"ranking": "1", "distance": "0.173799", "rankedImage": "V209050_p3.png"}, 
##            {"ranking": "2", "distance": "0.177393", "rankedImage": "V210290_p4.png"}, 
##            {"ranking": "3", "distance": "0.177911", "rankedImage": "V210261_p3.png"}, 
##            {"ranking": "4", "distance": "0.178684", "rankedImage": "V209071_p1.png"}, 
##            {"ranking": "5", "distance": "0.185251", "rankedImage": "V209075_p2.png"}
##        ],
##        "queryImage" : "V209046_p3.png",
##        "rankSize" : 5
##    },{
##        "images": [
##            {"ranking": "1", "distance": "0.173799", "rankedImage": "V209050_p3.png"}, 
##            {"ranking": "2", "distance": "0.177393", "rankedImage": "V210290_p4.png"}, 
##            {"ranking": "3", "distance": "0.177911", "rankedImage": "V210261_p3.png"}, 
##            {"ranking": "4", "distance": "0.178684", "rankedImage": "V209071_p1.png"}, 
##            {"ranking": "5", "distance": "0.185251", "rankedImage": "V209075_p2.png"}
##        ],
##        "queryImage" : "V209046_p3.png",
##        "rankSize" : 5
##    }]

##with open('dataFeatures.json', 'r')
