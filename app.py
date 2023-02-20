import xmltodict
import pprint
from PIL import Image
import numpy as np
import os

files = os.listdir("./annotations")

if not os.path.exists("./processed/helmet"):
    os.makedirs("./processed/helmet")

    
if not os.path.exists("./processed/nohelmet"):
    os.makedirs("./processed/nohelmet")

x = 0
for fileName in files:
    file = open('./annotations/'+fileName, 'rt')
    my_dict = xmltodict.parse(file.read())
    file.close()

    image = Image.open("./images/"+my_dict["annotation"]["filename"])
    dicObject = my_dict["annotation"]["object"]

    objType = type(dicObject) == type(list())

    if objType:
        nObjects = len(dicObject)
    else:
        nObjects = 1

    for i in range(nObjects):

        if objType:
            name = dicObject[i]["name"]
            arr = list(dicObject[i]["bndbox"].values())
        else:
            name = dicObject["name"]
            arr = list(dicObject["bndbox"].values())

        intArr = list(map(int,arr))

        length = abs(intArr[0]-intArr[2])
        height = abs(intArr[1]-intArr[3])

        if not ((length > 30 and length < 70) and (height > 30 and height < 70)):
            break

        img = image.crop(intArr)

        sqrWidth = np.ceil(np.sqrt(img.size[0]*img.size[1])).astype(int)
        img2 = img.resize((sqrWidth, sqrWidth))
        img3 = img2.resize((50, 50))

        if name == "helmet":
            # img3.save("./processed/helmet/"+str(x)+".jpeg")
            print("helmet")
        else:
            img3.save("./processed/nohelmet/"+str(x)+".jpeg")
        
        x += 1
