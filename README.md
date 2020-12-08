# Contextual-Information-ReID-Outdoor-Environments
Repository containing the experiments performed during the M.S. degree in Computer Science, as well as the results obtained

Project Structure and Content By Steps of Development:

# 1.- Video to frames conversion:
## 1.1.- Used ffmeg -i 1Original Videos/VID_20191009_172129.mp4 fps=30 V1%05d.png to produce a folder with the images of the first video in a folder with the name VID_20191009_172129
## 1.2.- Used ffmeg -i 1Original Videos/IMG_1741.avi fps=30 V2%05d.png to produce a folder with the images of the second video in a folder with the name IMG_1741
## 1.3.- Used ffmeg -i 1Original Videos/VID_20191009_17051334.mp4 fps=30 V3%05d.png to produce a folder with the images of the third video in a folder with the name VID_20191009_170513034
## 1.4.- Moved the generated folders to the 3Unlabeled Data Folder.
## 1.5.- Moved the content of the three folders to the folder Unlabeled Data/Mixed Data

# 2.- Images Boxing Process:
## 2.1.- in the folder 2Identities Boxing/PyTorch-YOLOv3/ run the following command to install all the required libraries.
	sudo pip3 install -r requirements.txt	
## 2.2.- Download pretrained weights
	cd weights/
	bash download_weights.sh
## 2.3.- Execute detect.py, to produce the boxes in the images in the output/boxed folder, and then crop the images and save the cropped versions directly in the output folder, as follows:
	python3 detect.py --image_folder 3UnlabeledData/MixedData

# 3.- Data Labeling Process:
## 3.1.- 3Unlabeled Data/output/ -> Contains original images of persons only.
## 3.2.- Move to the folder 6ReIDModels/person-reid-triplet-loss-baseline and from there: 	
	Execute: 4Scripts/Data Labeling Process/GenerateDescriptorFile.py
	Produces: 4Scripts/Data Labeling Process/imagesDesc2.txt which is a csv file containing all the images in the dataset, but processed through the first model-
## 3.3.- Using Chinese whispers clustering algorithm group the images according to the result obtained by this clustering algorithm:
	Execute: Inside of the 4Scripts/Data Labeling folder execute as follows ./GenerateClusters.py ./imagesDesc2.txt ../../5Labeled Data/Clases/
    	Produces: -> Creates the Classes folder and their subfolders
    	Clases/n/ -> Folders for each class clustered by the previous command.
## 3.4.- Manual revision of the images on each folder and move the ones not corresponding to another folder, to repeat clustering process in it.
	Execute: 4Scripts/Data Labeling Process/ClusterVerification.py n
    	Produces: -> Moves the verified cluster images to its corresponding folder after visual verification and correction.
## 3.5.- Execute: 4Scripts/Data Labeling Process/PhotosUnionAndRenaming.py n(Initial Folder) m(Final Folder)
    	Produces: -> Renames the images according to the folder they are in, and move them to the /labeledNew/ Folder.
    	labeledNew/ -> Images with corrected name according to proper identities.

# 4.- Embedding Data Generation.
## 4.1 Model 1
For the first model, a pre-trained weights file was used, trained over the market1501 dataset.
### 4.1.1.- Move to the folder 6ReIDModels/person-reid-triplet-loss-baseline and from there:
		Execute: 4Scripts/Contextual Information inclusion/infer_images_example.py --model_weight_file ./market1501_stride1/model_weight.pth
    		Produces: -> a json file containing the descriptor features of the images after being processed by the NN. As well as the images where they belong to. Saved in the folder 7Data Features

    		dataFeatures.json -> a json file with images data in the form of 
    		{
    		'images' : [{
        		'imageName' : 'VCXXXXXX_pI.png',
        		'features' : [ARRAY WITH 2048 features each]
        		}]
    		}

### 4.1.2.- Execute: 4Scripts/Contextual Information inclusion/marks_changes.py.
		This adds to the data the contextual information, including extra information in case such data is missing.

    		Produces: -> same dataFeatures.json file, but with the information in the following structure.
    		dataFeatures.json -> a json file with images data in the form of
    		{
    		'images' : [{
        		'camera' : (int) 1, 2 or 3
        		'imageName' : 'VCXXXXXX_pI.png',
        		'features' : [ARRAY WITH 2048 features each],
        		'latitude' : (float) latitude,
        		'longitude' : (float) longitude,
        		'time' : (string) date and time of picture,
        		'precipIntensity' : value of raining intensity in that moment,
        		'temperature' : value of temperature in that moment,
        		'humidity' : value of humidity in that moment,
        		'pressure' : value of pressure in that moment,
        		'windSpeed' : value of wind Speed in that moment,
        		'windGust' : value of wind Gust in that moment,
        		'cloudCover' : tells if clouds were covering the area,
        		'visibility' : visibility range
        		}]
    		}

### 4.1.3.- Manually copy the generated dataFeatures.json file to the 8Data Features and Context Jsons

## 4.2 Model 2
For the second model, the model was trained over with our data set, prior to extracting the features and adding the contextual information.
### 4.2.1.-	Execute: 4/Scripts/Model 2 embedding generation process/NewImagesInFolders.py:
		It takes the labeled images in the LabeledNew Folder and separates it in a train set, a test set, and a query set, in order to train with this the second model MGN.
		Produces: A new folder named LabeledNewFolders containing three different subfolders:
	 	bounding_box_train/    (containing the 80% of the ids in the data)
	 	bounding_box_test/     (containing the 20% of the ids in the data)
	 	query/                 (containing every image, since the approach was to use this to produce a ranking of every image in the data)
### 4.2.2.- Train the model according to the previously defined partition in the data.
		Move to the folder 6ReID Models/ReID-MGN/
		Execute: 6ReID Models/ReID-MGN/main.py --mode train --data_path ../../5Labeled Data/labeledNewFolders/
		Produces: A folder 6ReID Models/ReID-MGN/weights/ containing the weights of the trained model.

### 4.2.3.- Use the trained model to extract features and save it.
		Move to the folder 6ReID Models/ReID-MGN/	
		Execute: 6ReID Models/ReID-MGN/main.py --mode extract --data_path ../../5Labeled Data/labeledNewFolders/ --weight 6ReID Models/ReID-MGN/weights/model_100.pt
		Produces: A csv file named MGNFeatures.csv in the folder 7Data Features/ containing the descriptors of the images in the dataset. along with its name, in the form |feat0|feat1|...|feat2047|imageName|
### 4.2.4.- Move to the folder 4Scripts/Contextual Information Inclusion and from there:
		Execute: 4Scripts/Contextual Information Inclusion/infer_images.py
    		Produces: -> a json file containing the descriptor features of the images after being processed by the NN. As well as the images where they belong to. Saved in the folder 7Data Features.

    		dataMGNFeatures.json -> a json file with images data in the form of 
    		{
    		'images' : [{
        		'imageName' : 'VCXXXXXX_pI.png',
        		'features' : [ARRAY WITH 2048 features each]
        		}]
    		}
### 4.2.5.- Execute: 4Scripts/Context Information inclusion/marks_changesMGN.py.
		This adds to the data the contextual information, including extra information in case such data is missing.
    		Produces: -> same dataMGNFeatures.json file, but with the information in the following structure.
    
    		dataMGNFeatures.json -> a json file with images data in the form of
    		{
    		'images' : [{
        		'camera' : (int) 1, 2 or 3
        		'imageName' : 'VCXXXXXX_pI.png',
        		'features' : [ARRAY WITH 2048 features each],
        		'latitude' : (float) latitude,
        		'longitude' : (float) longitude,
        		'time' : (string) date and time of picture,
        		'precipIntensity' : value of raining intensity in that moment,
        		'temperature' : value of temperature in that moment,
        		'humidity' : value of humidity in that moment,
        		'pressure' : value of pressure in that moment,
        		'windSpeed' : value of wind Speed in that moment,
        		'windGust' : value of wind Gust in that moment,
        		'cloudCover' : tells if clouds were covering the area,
        		'visibility' : visibility range
        		}]
    		}
### 4.2.6.- Manually copy the generated dataMGNFeatures.json file to the 8Data Features and Context Jsons
## 4.3 Model 3
### 4.3.1.- Execute 6ReID Models/MLFNModel.ipynb. The first part makes use of dataFeatures.json from model 1, to obtain the images names, ids and cameras. Such information is provided to the code, creating an array of image names for training and for testing of the model. 

After the model is trained, the code allows to transform to features any image we require, so we process every image in the image data set and save the features.

When the training is finished, a dataMLFNfeatures.json file is produced including the already existing contextual information from the original file.
	
		Produces:
    		dataFeaturesMLFN.json -> a json file with images data in the form of
    		{
    		'images' : [{
        		'camera' : (int) 1, 2 or 3
        		'imageName' : 'VCXXXXXX_pI.png',
        		'features' : [ARRAY WITH 2048 features each],
        		'latitude' : (float) latitude,
        		'longitude' : (float) longitude,
        		'time' : (string) date and time of picture,
        		'precipIntensity' : value of raining intensity in that moment,
        		'temperature' : value of temperature in that moment,
        		'humidity' : value of humidity in that moment,
        		'pressure' : value of pressure in that moment,
        		'windSpeed' : value of wind Speed in that moment,
        		'windGust' : value of wind Gust in that moment,
        		'cloudCover' : tells if clouds were covering the area,
        		'visibility' : visibility range
        		}]
    		}

# 5.- Neural Network Input Formating.
## 5.1.- Model 1
### 5.1.1 	Execute: 4Scripts/Contextual Information inclusion/inputNNGenerator.py
	Produces: A csv file named data3.csv in the folder 9Data Features and Context csv containing the data in the format the neural network expects it to be.
## 5.2.- Model 2
### 5.2.1 	Execute: 4Scripts/Contextual Information inclusion/inputNNGeneratorMGN.py
	Produces: A csv file named data3MGN.csv in the folder 9Data Features and Context csv containing the data in the format the neural network expects it to be.
## 5.3.- Model 3
### 5.3.1 	Change the commented code sections in the file 4Scripts/Contextual Information inclusion/inputNNGenerator.py
### 5.3.2 	Execute: 4Scripts/Contextual Information inclusion/inputNNGenerator.py
	Produces: A csv file named data3MLFN.csv in the folder 9Data Features and Context csv containing the data in the format the neural network expects it to be.

# 6.- Siamesse Network Training
## 6.1 .- 	Execute: ReidNueralNetwork3.ipynb 
	Produces: the results and the evaluation obtained by the model.
