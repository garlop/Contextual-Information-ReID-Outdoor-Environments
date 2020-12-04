# coding=utf-8
import json
import re
import os
import pickle
from Tkinter import *

currIdentity = ""
accepted = False
comparingImages = []
queryImage = ""

class Application(Frame):
    def accept(self, root):
	global accepted 
        accepted = True
        root.destroy()

    def reject(self, root):
	global accepted 
        accepted = False
        root.destroy()

    def createWidgets(self, root):
        self.Reject = Button(self)
        self.Reject["text"] = "Reject"
        self.Reject["fg"]   = "red"
        self.Reject["command"] =  lambda: self.reject(root)

        self.Reject.pack({"side": "left"})

        self.Accept = Button(self)
        self.Accept["text"] = "Accept"
        self.Accept["fg"] = "blue"
        self.Accept["command"] = lambda: self.accept(root)

        self.Accept.pack({"side": "left"})

    def center(self, root):
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)
        self.center(master)

def assignIdentity(currentName, newIdentity):
    ## Rename image
    global comparingImages
    print("renaming the image")
    end = currentName.find('_p')
    nameWithoutId = currentName[0:end]
   
    print(nameWithoutId)    
    print(newIdentity)
    print(currentName)

    if (nameWithoutId+"_p"+newIdentity+".png" == currentName):
        return newIdentity.zfill(5)

    os.rename(r'/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/'+currentName,r'/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/'+nameWithoutId+"_p"+newIdentity+".png")

    ##Then the value is updated in the filesNames.pkl file
    print("updating renamed image in the filesNames.pkl file")
    with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'rb') as f:
        partitions = pickle.load(f)
        im_names = partitions['{}_im_names'.format('test')]
        new_im_names = im_names[:]
        new_im_names[im_names.index(currentName)] = nameWithoutId+"_p"+newIdentity+".png"

        partitions['{}_im_names'.format('test')] = new_im_names
    f.close()

    with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'w') as f:
        pickle.dump(partitions, f)
    f.close()

    for image in comparingImages:
        if image["rankedImage"] == currentName:
            comparingImages[comparingImages.index(image)]["rankedImage"] = nameWithoutId+"_p"+newIdentity+".png"
            break

    numNewIdentity = int(newIdentity)
    newIdentity = str(numNewIdentity + 1)
    return newIdentity.zfill(5)


##Ejecuta el ReID obteniendo una lista de 100 imágenes.

##Asigna una identidad propia a la imagen query de la consulta.
with open('/home/dell_mserver_01/Escritorio/person-reid-triplet-loss-baseline/rankedImages.json') as json_file, open('currId.txt') as currId:
    global comparingImages
    global currIdentity
    global queryImage
    data = json.load(json_file)
    queryImage = data['queryImage']
    comparingImages = data['images']

    start = queryImage.find('_p') + 2
    end = queryImage.find(".") 
    imageId = queryImage[start:end]
    print(imageId)
    temp = currId.read().replace('\n', '')
    currIdentity = temp
    if len(imageId) < 2:
        print("assigning identity to query image if needed")
        currIdentity = assignIdentity(queryImage, currIdentity)
        queryImage = queryImage[0:start-2]+"_p"+temp+".png"
        print

with open('currId.txt', 'w') as f:
    f.seek(0)
    f.write(currIdentity)
    f.truncate()
    f.close()

def reassignIdentities(prevQueryIdentity, newQueryIdentity):
    global queryImage
    #First update identity on query image
    print("first update identity on query image")
    start1 = queryImage.find('_p') + 2
    end1 = queryImage.find(".") 
    imageWithoutId = queryImage[0:start-2]
    print(imageWithoutId)
    imageId = queryImage[start:end]
    print(imageId)
    assignIdentity(queryImage, newQueryIdentity)
    queryImage = imageWithoutId+"_p"+newQueryIdentity+".png"
    print(queryImage)
    print("Then on each image in the set considered")
    #Then on each image in the set considered.
    for image in comparingImages:
        start2 = image["rankedImage"].find('_p') + 2
        end2 = image["rankedImage"].find(".")
        imageWithoutId = image["rankedImage"][0:start-2]
        print(imageWithoutId)
        imageId = image["rankedImage"][start:end]
        print(imageId)
        if prevQueryIdentity == imageId:
            assignIdentity(image["rankedImage"], newQueryIdentity)

##Visualizando en todo momento el queryImage y la foto de donde salió, así como el posible resultado coincidente y la imágen de donde salió este otro, permite elegir si se trata de la misma persona o no.

index = 1
for image in comparingImages:
    #First split picture, from picture with identity
    start = image["rankedImage"].find('_p') + 2
    end = image["rankedImage"].find(".")
    rankedWithoutId = image["rankedImage"][0:start-2]
    print(rankedWithoutId)
    rankedId = image["rankedImage"][start:end]
    print(rankedId)
    start2 = queryImage.find('_p') + 2
    end2 = queryImage.find('.') 
    nameWithoutId = queryImage[0:start2-2]
    print(nameWithoutId)
    nameId = queryImage[start2:end2]
    print(nameId)

    index = index + 1

    if nameId == rankedId:
        continue

    root = Tk()
    root.title("ReID Labeling image "+str(index)+" of "+str(len(comparingImages)))
    canvas = Canvas(root, width = 800, height = 800)      
    canvas.pack()      
    img1 = PhotoImage(file="/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/"+queryImage)
    img2 = PhotoImage(file="/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/"+image["rankedImage"])
    img3 = PhotoImage(file="/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/boxed/"+rankedWithoutId+".png")
    img4 = PhotoImage(file="/home/dell_mserver_01/Documentos/Luis/PyTorch-YOLOv3/output/boxed/"+nameWithoutId+".png")
    canvas.create_image(550,30, anchor=NW, image=img2)
    canvas.create_image(550,410, anchor=NW, image=img1)
    canvas.create_image(20,20, anchor=NW, image=img3)
    canvas.create_image(20,400, anchor=NW, image=img4)
    app = Application(master=root)
    app.mainloop()
    if accepted == True:
        ##3.2.- Si coincide, valida si la imagen ya tiene o no asigando un id nuevo.
        if len(rankedId) > 2:
            ##3.2.1.- Si ya lo tiene, actualiza el id de la imágen query que se usaba hasta ese momento, por el de la imagen encontrada, del mismo modo actualiza el id a todas las imágenes que fueron marcadas como coincidentes con dicho imagen query, por el id de la imagen encontrada. La asignación cambia el nombre de la imagen en la carpeta output, así como el valor asignado en el archivo fileNames.pkl
            print("accepted and id is new")
            reassignIdentities(nameId, rankedId)
        else:
            ##3.2.2.- Si no tiene id asignado, se le asigna a la imagen el id de la imagen query. La asignación cambia el nombre de la imagen en la carpeta output, así como el valor asignado en el archivo fileNames.pkl
            print("accepted and id is old")
            assignIdentity(image["rankedImage"], nameId)
    #else:
        #print("rejected")
        ##3.1.- Si la imágen no coincide, valida si la imagen ya tiene o no asignado un id nuevo.
        #if not(len(rankedId) > 2):
            #print(" and id is old")
            ##3.1.1.- Si la imagen no tiene id asignado, se le genera un nuevo id propio de acuerdo al valor global de ids asignados hasta ese momento. La asignación cambia el nombre de la imagen en la carpeta output, así como el valor asignado en el archivo fileNames.pkl
            ##currIdentity = assignIdentity(image["rankedImage"], currIdentity)

##4.- Se actualiza en filesNames.pkl las imagenes query, asignando como galery images, a aquellas ya tienen id asignado, y dejando como query images 100 imagenes que no tengan id asignado.

with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'rb') as f:
    partitions = pickle.load(f)
    marks = partitions['test_marks']
    im_names = partitions['{}_im_names'.format('test')]
    if marks[im_names.index(queryImage)] == 0:
        marks[im_names.index(queryImage)] = 1
    partitions['test_marks'] = marks
f.close()

with open('/home/dell_mserver_01/Escritorio/filesNames.pkl', 'w') as f:
    pickle.dump(partitions, f)
f.close()
