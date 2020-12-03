import pickle
import requests
import json
import os
import datetime
import re

"""
This is meant to be RUN ONLY ONCE, since it is the inclusion of location data to the info of images that is used for re-id
"""
"""with open('partitions.pkl', 'rb') as f:
    partitions = pickle.load(f)
    im_names = partitions['{}_im_names'.format('test')]
    latitudes = []
    longitudes = []
    time = []
    for i in range(0, len(im_names)):
        latitudes.append('19.3554')
        longitudes.append('-99.1333')
        time.append('2018-10-24T19:06:32')
    newValues = {
    'latitude' : latitudes,
    'longitude' : longitudes,
    'time' : time
    }
    partitions.update(newValues)
f.close()

with open('partitions.pkl', 'w') as f:
    pickle.dump(partitions, f)
f.close()"""

"""
COMPROBATION THAT THE COORDINATES WERE SAVED IN THE PICKE FILE
"""
"""
with open('partitions.pkl', 'rb') as f:
    partitions = pickle.load(f)
    im_names = partitions['{}_im_names'.format('test')]
    marks = partitions['test_marks']
    countQ= 0
    countMQ = 0
    latitudes = partitions['latitude']
    longitudes = partitions['longitude']
    time = partitions['time']
    for i in range(0, len(im_names)):
        if(marks[i] == 0):
            print("queryImg", im_names[i])
	    print("latitude", latitudes[i])
            print("latitude", longitudes[i])
            print("latitude", time[i])
f.close()
"""

def one(img_name):
    camera = 1            
    latitude = "25.6515556"	
    longitude = "-100.289125"
    elapsedTime = float(img_name[2:6])/30
    initialTime = '2019-10-09T17:05:13'
    initialTimeDT = datetime.datetime.strptime(initialTime,"%Y-%m-%dT%H:%M:%S")
    finalDT = initialTimeDT + datetime.timedelta(seconds = elapsedTime)
    time = datetime.datetime.strftime(finalDT ,"%Y-%m-%dT%H:%M:%S")
    return camera, latitude, longitude, time

def two(img_name):
    camera = 2
    latitude = "25.651451"	
    longitude = "-100.289315"
    elapsedTime = float(img_name[2:6])/30
    initialTime = '2019-10-09T17:06:47'
    initialTimeDT = datetime.datetime.strptime(initialTime,"%Y-%m-%dT%H:%M:%S")
    finalDT = initialTimeDT + datetime.timedelta(seconds = elapsedTime)
    time = datetime.datetime.strftime(finalDT ,"%Y-%m-%dT%H:%M:%S") 
    return camera, latitude, longitude, time

def three(img_name):
    camera = 3
    latitude = "25.650791"	
    longitude = "-100.288979"
    elapsedTime = float(img_name[2:6])/30
    initialTime = '2019-10-09T17:06:26'
    initialTimeDT = datetime.datetime.strptime(initialTime,"%Y-%m-%dT%H:%M:%S")
    finalDT = initialTimeDT + datetime.timedelta(seconds = elapsedTime)
    time = datetime.datetime.strftime(finalDT ,"%Y-%m-%dT%H:%M:%S")
    return camera, latitude, longitude, time

def switch(camId):
    switcher = {
        '1': one,
        '2': two,
        '3': three
    }
    function = switcher.get(camId)
    return function

dirname = os.path.dirname(os.path.abspath(__file__))
filename = dirname+'/person-reid-triplet-loss-baseline/dataFeatures.json'

with open(filename) as json_file:
    data = json.load(json_file)

for i in range(0,len(data['images'])):
    img = data['images'][i]
    img_name = img['imageName']
    features = img['features']
    print("reviewing an image", img['imageName'])

    try:
        testingLatitude = img['latitude']
        print("testingLatitude is",testingLatitude)
    except:
        testingLatitude = ""
        
    if(testingLatitude == ""):
        imageName = re.search('V(.+?).png', img_name).group(0)
        retrieveValues = switch(imageName[1])
        camera, latitude, longitude, time = retrieveValues(imageName)
           
        response = requests.get('https://api.darksky.net/forecast/9c573bc1f71fbd78a0541d7891ecb594/'+latitude+','+longitude+','+time, params={'exclude':'hourly,daily,flags', 'units':'si'},)
        json_data = {}
        if response.status_code == 200:
            json_data = response.json()
            precipIntensity = json_data['currently']['precipIntensity']
            temperature = json_data['currently']['temperature']
            humidity = json_data['currently']['humidity']
            pressure = json_data['currently']['pressure']
            windSpeed = json_data['currently']['windSpeed']
            windGust = json_data['currently']['windGust']
            cloudCover = json_data['currently']['cloudCover']
            visibility = json_data['currently']['visibility']
            print("saved data from API")
        else:
            precipIntensity = ''
            temperature = ''
            humidity = ''
            pressure = ''
            windSpeed = ''
            windGust = ''
            cloudCover = ''
            visibility = ''
            print("API returned error, saving nothing")

        dataObtained = { 
            'camera' : camera,
            'latitude' : latitude,
            'longitude' : longitude,
            'time' : time,
            'precipIntensity' : precipIntensity,
            'temperature' : temperature,
            'humidity' : humidity,
            'pressure' : pressure,
            'windSpeed' : windSpeed,
            'windGust' : windGust,
            'cloudCover' : cloudCover,
            'visibility' : visibility}

        img.update(dataObtained)
        data['images'][i] = img
        print("updating values obtained")

    else:
        try:
            precipitation = img['precipIntensity']
            print("precipitation is",precipitation)
        except:
            precipitation = ""

        if precipitation == "":           
            imageName = re.search('V(.+?).png', img_name).group(0)
            retrieveValues = switch(imageName[1])
            camera, latitude, longitude, time = retrieveValues(imageName)
            
            response = requests.get('https://api.darksky.net/forecast/9c573bc1f71fbd78a0541d7891ecb594/'+latitude+','+longitude+','+time, params={'exclude':'hourly,daily,flags', 'units':'si'},)
            json_data = {}
            if response.status_code == 200:
                json_data = response.json()
                precipIntensity = json_data['currently']['precipIntensity']
                temperature = json_data['currently']['temperature']
                humidity = json_data['currently']['humidity']
                pressure = json_data['currently']['pressure']
                windSpeed = json_data['currently']['windSpeed']
                windGust = json_data['currently']['windGust']
                cloudCover = json_data['currently']['cloudCover']
                visibility = json_data['currently']['visibility']
                print("saved data from API")
            else:
                precipIntensity = ''
                temperature = ''
                humidity = ''
                pressure = ''
                windSpeed = ''
                windGust = ''
                cloudCover = ''
                visibility = ''
                print("API returned error, saving nothing")

                dataObtained = { 
                    'camera' : camera,
                    'latitude' : latitude,
                    'longitude' : longitude,
                    'time' : time,
                    'precipIntensity' : precipIntensity,
                    'temperature' : temperature,
                    'humidity' : humidity,
                    'pressure' : pressure,
                    'windSpeed' : windSpeed,
                    'windGust' : windGust,
                    'cloudCover' : cloudCover,
                    'visibility' : visibility}

                img.update(dataObtained)
                data['images'][i] = img
                print("updating values obtained")
                break

            dataObtained = { 
                'camera' : camera,
                'latitude' : latitude,
                'longitude' : longitude,
                'time' : time,
                'precipIntensity' : precipIntensity,
                'temperature' : temperature,
                'humidity' : humidity,
                'pressure' : pressure,
                'windSpeed' : windSpeed,
                'windGust' : windGust,
                'cloudCover' : cloudCover,
                'visibility' : visibility}

            img.update(dataObtained)
            data['images'][i] = img
            print("updating values obtained")

json_file.close()

with open(filename, 'w') as jsonfile:
    json.dump(data, jsonfile)
jsonfile.close()
