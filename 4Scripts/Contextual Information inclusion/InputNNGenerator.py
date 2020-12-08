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
    #imageName = "../../5Labeled Data/labeledNew/"+imageName
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

dictionary = defaultdict(list)
isEmptyField = False

with open('../../8Data Features and Context Jsons/dataFeatures.json', 'r') as imagesFeatures:
#with open('../../8Data Features and Context Jsons/dataFeaturesMLFN.json', 'r') as imagesFeatures:
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

IFeatHeaders=[]

for i in range(0,2048):
#for i in range(0,1024):
    print(i)
    IFeatHeaders.append("IFeat"+str(i))

with open('../../9Data Features and Context csv/data3.csv', 'a+', newline='') as csvData:
#with open('../../9Data Features and Context csv/data3MLFN.csv', 'a+', newline='') as csvData:
    writer = csv.writer(csvData, delimiter='|')
    headers = ['C', 'Lat', 'Long']
    headers.extend(feat for feat in IFeatHeaders)
    headers.extend(['Time', 'preInt', 'temp', 'hum', 'press', 'WindS', 'WindG', 'CloudC', 'Visb', 'Id'])
    headers.extend(['I'])
    writer.writerow(headers)
    print(headers)  
csvData.close()

for image in images:
    imageNameParts = image["imageName"].split("/")
    imageNameWhole = image["imageName"]
    ImageName = imageNameParts[-1:][0]
    print(ImageName)
    m = re.search('_p[0-9]*',ImageName)
    Id = m.group(0)[2:]
    C = ImageName[1]
    count = count + 1
    print("saving data of image:"+ImageName+" image "+str(count)+" of "+str(len(images)))
    ILat, ILong, IFeat, ITime, IpreInt, Itemp, Ihum, Ipress, IWindS, IWindG, ICloudC, IVisb = searchImageMetaData(imageNameWhole, dictionary)
    with open('../../9Data Features and Context csv/data3.csv', 'a+', newline='') as csvData:
#    with open('../../9Data Features and Context csv/data3MLFN.csv', 'a+', newline='') as csvData:
        if Itemp == "":
            print("row Empty, not saving")
        else:
            writer = csv.writer(csvData, delimiter='|')
            values = [C, ILat, ILong]
            values.extend(feat for feat in IFeat)
            values.extend([ITime, IpreInt, Itemp, Ihum, Ipress, IWindS, IWindG, ICloudC, IVisb, Id])
            values.extend([imageName])
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
