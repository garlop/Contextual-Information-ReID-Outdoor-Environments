# coding=utf-8
import os
from Tkinter import *
from os import listdir
from os.path import isfile, join
import shutil
import random
from distutils.dir_util import copy_tree

if len(sys.argv) != 2:
    print(
        "Call this program like this:\n"
        "   ./ClusterVerification.py 23(classId)")
    exit()

global abort
global classID

classID = int(sys.argv[1])

accepted = False
abort = False
id_Indeterminado = "indeterminado"

class RandomImage(Frame):
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
        self.center(master)

class Application(Frame):
    def accept(self, root):
        global accepted
        accepted = True
        root.destroy()

    def reject(self, root):
        global accepted
        accepted = False
        root.destroy()

    def abort(self, root):
        global abort
        abort = True
        print("process aborted, all the images were sent to indeterminate class")
        root.destroy()

    def randomImage(self, root):
        global auximg1
        global auximg2
        global auximg3
        global imagesInClass
        global classID
        tmp = imagesInClass[:]
        result = [tmp.pop(random.randrange(len(tmp))) for _ in range(3)]
        auximg1 = result[0]
        auximg2 = result[1]
        auximg3 = result[2]
        rimage = Tk()
        rimage.title("Random Image of class "+str(classID))
        canvas = Canvas(rimage, width = 800, height = 800)    
        canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
                        text=auximg1) 
        canvas.create_text(500,10,fill="darkblue",font="Times 20 italic bold",
                        text=auximg2) 
        canvas.create_text(500,400,fill="darkblue",font="Times 20 italic bold",
                        text=auximg3)
        canvas.pack()      
        img1 = PhotoImage(master = canvas, file="../../3Unlabeled Data/output/"+auximg1)
        img2 = PhotoImage(master = canvas, file="../../3Unlabeled Data/output/"+auximg2)
        img3 = PhotoImage(master = canvas, file="../../3Unlabeled Data/output/"+auximg3)
        print(auximg1)
        print(auximg2)
        print(auximg3)
        canvas.create_image(550,30, anchor=NW, image=img2)
        canvas.create_image(550,410, anchor=NW, image=img3)
        canvas.create_image(20,20, anchor=NW, image=img1)
        app = RandomImage(master=root)
        app.mainloop()

    def createWidgets(self, root):
        global imagesInClass
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

        self.Abort = Button(self)
        self.Abort["text"] = "Abort"
        self.Abort["fg"] = "blue"
        self.Abort["command"] = lambda: self.abort(root)

        self.Abort.pack({"side": "left"})

        if len(imagesInClass) > 2:
            self.RandomImage = Button(self)
            self.RandomImage["text"] = "Random Sample"
            self.RandomImage["fg"] = "gray"
            self.RandomImage["command"] = lambda: self.randomImage(root)
            
            self.RandomImage.pack({"side":"left"})
 
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

def moveImage(currentIdClass, newIdClass, imageName):
    shutil.move('../../5Labeled Data/Clases/'+str(currentIdClass)+"/"+imageName, '../../5Labeled Data/Clases/'+str(newIdClass)+"/"+imageName)

def mixClasses(stClass1, endClass2):
    merged_folder_path = '../../5Labeled Data/Clases/'+str(endClass2)+"/"
    copy_tree('../../5Labeled Data/Clases/'+str(stClass1)+"/", merged_folder_path)
    shutil.rmtree('../../5Labeled Data/Clases/'+str(stClass1)+"/")

global imagesInClass

if os.path.isdir('../../5Labeled Data/Clases/'+str(classID)+"/"):
    imagesInClass = [f for f in listdir('../../5Labeled Data/Clases/'+str(classID)+"/") if isfile(join('../../5Labeled Data/Clases/'+str(classID)+"/", f))]
    global currentImage
    global auximg1
    global auximg2
    global auximg3

    index = 0
    for currentImage in imagesInClass:
        root = Tk()
        root.title("Verification "+str(currentImage)+" image "+str(index+1)+" of "+str(len(imagesInClass)))
        index = index + 1
        canvas = Canvas(root, width = 500, height = 500)      
        canvas.pack()      
        img1 = PhotoImage(file="../../5Labeled Data/Clases/"+str(classID)+"/"+currentImage)
        canvas.create_image(50,50, anchor=NW, image=img1)
        app = Application(master=root)
        app.mainloop()
        if abort == True:
            print("aborted")
            mixClasses(classID, id_Indeterminado)
            break
        else:
            if accepted == True:
                print("accepted")
	        #Nothing at all
            else:
                print("rejected")
                moveImage(classID, id_Indeterminado, currentImage)
else:
    print("The requested class folder do not exists")
