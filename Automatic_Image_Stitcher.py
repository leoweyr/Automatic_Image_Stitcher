import os

from PIL import Image, ImageDraw
import easygui as g
import webbrowser

VERSION = "1.0.0"
SWNAME = "Automatic Image Stitcher " + VERSION

g_isRecyclingMaterial = False
g_stitchingRoute_macro_count_sum = 0

class ImageGather:
    def __init__(self,path):
        self.m_path = path
        self.m_imagesCount = len(os.listdir(path))
        self.m_namedSerialization = 0
        self.m_namedSuffix = None
        if(self.m_imagesCount == 0):
            self.m_imageIDFirst = 1
            self.m_imageIDNext = self.m_imageIDFirst
            self.m_imageSelect = self.m_imageIDFirst
        else:
            if(self.GetNamedRule() == False):
                self .isGetNamedRule = False
            else:
                self.isGetNamedRule = True
                self.m_imageIDNext = self.m_imageIDFirst + self.m_imagesCount
                self.m_imageSelect = self.m_imageIDFirst

    def GetNamedRule(self):
        imageNames = os.listdir(self.m_path)
        if(self.m_imagesCount > 1):
            cheakPos = 0
            isDifferentPos = True
            while True:
                try:
                    int(imageNames[0][cheakPos])
                    int(imageNames[1][cheakPos])
                except:
                    if(isDifferentPos == False):
                        isDifferentPos = True
                    elif(cheakPos > len(imageNames[0]) or cheakPos > len(imageNames[1])):
                        return False
                    cheakPos += 1
                else:
                    if(imageNames[0][cheakPos] != imageNames[1][cheakPos]):
                        if(isDifferentPos == False):
                            differentPos = differentPos_breakup
                        else:
                            differentPos = cheakPos
                        break
                    elif(imageNames[0][cheakPos] == imageNames[1][cheakPos]):
                        if(isDifferentPos == True):
                            isDifferentPos = False
                            differentPos_breakup = cheakPos
                        cheakPos += 1
            if(differentPos > 1):
                self.m_namedPrefix = str(imageNames[0][0:differentPos])
            elif(differentPos == 1):
                self.m_namedPrefix = str(imageNames[0][0])
            else:
                self.m_namedPrefix = ""
            cheakPos = differentPos
            cheakMode = 0
            includeIntCount = 0
            isSerial = False
            while (cheakMode < 2):
                for imageName in imageNames:
                    if(cheakMode == 0):
                        if (differentPos > 1):
                            namedPrefix = str(imageName[0:differentPos])
                        elif (differentPos == 1):
                            namedPrefix = str(imageName[0])
                        else:
                            namedPrefix = ""
                        if(namedPrefix != self.m_namedPrefix):
                            return False
                        try:
                            int(imageName[cheakPos])
                        except:
                            pass
                        else:
                            includeIntCount += 1
                            if(imageName[differentPos] == "0"):
                                try:
                                    int(imageName[differentPos+1])
                                except:
                                    pass
                                else:
                                    isSerial = True
                    elif(cheakMode == 1):
                        cheakPos = differentPos
                        isEnd = False
                        intCount = 0
                        while (isEnd == False):
                            try:
                                int(imageName[cheakPos])
                            except:
                                isEnd = True
                                if(self.m_namedSuffix == None):
                                    self.m_namedSuffix = imageName[cheakPos:]
                                elif(self.m_namedSuffix != imageName[cheakPos:]):
                                    return False
                            else:
                                intCount += 1
                                cheakPos += 1
                        if(isSerial == True and intCount > self.m_namedSerialization):
                            self.m_namedSerialization = intCount
                if(includeIntCount == 0):
                    return False
                cheakMode += 1
        else:
            intCount = 0
            cheakPos = 0
            isGetDifferentPos = False
            isSerial = False
            while True:
                try:
                    int(imageNames[0][cheakPos])
                except:
                    if(cheakPos > 0):
                        try:
                            int(imageNames[0][cheakPos - 1])
                        except:
                            pass
                        else:
                            self.m_namedSuffix = imageNames[0][cheakPos:]
                            self.m_imageIDFirst = imageNames[0][cheakPos - 1]
                            break
                    elif(len(imageNames[0]) == 1):
                        break
                else:
                    intCount += 1
                    if(isGetDifferentPos == False):
                        if(cheakPos > 1):
                            self.m_namedPrefix = imageNames[0][0:cheakPos]
                        elif(cheakPos == 1):
                            self.m_namedPrefix = imageNames[0][0]
                        else:
                            self.m_namedPrefix = ""
                        isGetDifferentPos = True
                    else:
                        if(imageNames[0][cheakPos] == "0"):
                            try:
                                int(imageNames[0][cheakPos + 1])
                            except:
                                pass
                            else:
                                isSerial = True

                cheakPos += 1
            if(intCount == 0):
                return False
            if(isSerial == True):
                self.m_namedSerialization = intCout
        intMin = 0
        while (intMin < 10):
            if (self.m_namedPrefix + str("0"*(self.m_namedSerialization - 1)) + str(intMin) + self.m_namedSuffix in imageNames):
                self.m_imageIDFirst = intMin
                break
            intMin += 1
        return True

    def GetNamedSerial(self,number):
        if(self.m_namedSerialization == 0):
            return str(number)
        else:
            namedSerialization = 0
            namedSerial = ""
            while (namedSerialization < self.m_namedSerialization - len(str(number))):
                namedSerial += "0"
                namedSerialization += 1
            return namedSerial + str(number)

    def Add(self,image):
        image.save(self.m_path + "\\" + self.m_namedPrefix + self.GetNamedSerial(self.m_imageIDNext) + self.m_namedSuffix)
        self.m_imageIDNext += 1

    def CoverLast(self,image):
        image.save(self.m_path + "\\" + self.m_namedPrefix + self.GetNamedSerial(self.m_imageIDNext - 1) + self.m_namedSuffix)

    def SelectReset(self):
        self.m_imageSelect = self.m_imageIDFirst

    def SelectPresent(self):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + self.GetNamedSerial(self.m_imageSelect) + self.m_namedSuffix)
        return image

    def SelectLast(self):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + self.GetNamedSerial(self.m_imageIDNext - 1) + self.m_namedSuffix)
        return image

    def SelectAndRoll(self,isSelectLoop=g_isRecyclingMaterial):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + self.GetNamedSerial(self.m_imageSelect) + self.m_namedSuffix)
        if(isSelectLoop == True and self.m_imageSelect == self.m_imageIDNext):
            self.SelectReset()
        self.m_imageSelect += 1
        return image

def StitchedImages_vertical(imgFront,imgBack):
    if(imgFront.size[0] > imgBack.size[0]):
        stitchedImages_width = imgFront.size[0]
    else:
        stitchedImages_width = imgBack.size[0]
    stitchedImages_height = imgFront.size[1] + imgBack.size[1]
    stitchedImages = Image.new("RGB",(stitchedImages_width,stitchedImages_height))
    stitchedImages.paste(imgFront,(0,0))
    stitchedImages.paste(imgBack,(imgFront.size[0] - imgBack.size[0],imgFront.size[1])) #Extend to the bottom right.
    return stitchedImages

def StitchedImages_horizontal(imgFront,imgBack):
    if (imgFront.size[1] > imgBack.size[1]):
        stitchedImages_height = imgFront.size[1]
    else:
        stitchedImages_height = imgBack.size[1]
    stitchedImages_width = imgFront.size[0] + imgBack.size[0]
    stitchedImages = Image.new("RGB", (stitchedImages_width, stitchedImages_height))
    stitchedImages.paste(imgFront, (0, 0))
    stitchedImages.paste(imgBack, (imgFront.size[0], imgFront.size[1] - imgBack.size[1])) #TODO: Extend in a custom direction.
    return stitchedImages


def StitchImage(stitchingRoute,imageGather_basic,imageGather_generated):
    global g_isRecyclingMaterial
    global g_stitchingRoute_macro_count_sum
    imageGather_generated.m_namedPrefix = imageGather_basic.m_namedPrefix
    imageGather_generated.m_namedSerialization = imageGather_basic.m_namedSerialization
    imageGather_generated.m_namedSuffix = imageGather_basic.m_namedSuffix
    stitchingRouteCount = 0
    while True:
        stitchingRoute_macro = stitchingRoute.split(",")
        for stitchingRoute_micro in stitchingRoute_macro:
            try:
                stitchingRoute_micro.split(")")[1]
            except:
                stitchingRoute_micro_count = imageGather_basic.m_imagesCount
                isResize = False
            else:
                stitchingRoute_micro_count = int(stitchingRoute_micro.split(")")[1].split(":")[0])
                try:
                    stitchingRoute_micro.split(")")[1].split(":")[1]
                    stitchingRoute_micro.split(")")[1].split(":")[1].split("*")[1]
                except:
                    isResize = False
                else:
                    isResize = True
                    stitchingRoute_micro_imageSize_width = stitchingRoute_micro.split(")")[1].split(":")[1].split("*")[0]
                    stitchingRoute_micro_imageSize_height = stitchingRoute_micro.split(")")[1].split(":")[1].split("*")[1]
            try:
                stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0].split("(")[1]
            except:
                stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0]
            stitchingRoute_micro_cycle_each = stitchingRoute_micro_cycle.split("-")
            processedCount = 0
            while True:
                for processedUnit in stitchingRoute_micro_cycle_each:
                    try:
                        processedIDMax = int(processedUnit[1:])
                    except:
                        processedIDMax = 1
                    processID = 0
                    if (processedUnit[0] == "V"):
                        process = StitchedImages_vertical
                    elif (prcessUnit[0] == "H"):
                        process = StitchedImages_horizontal
                    while True:
                        if(processedCount < stitchingRoute_micro_count or processID < processedIDMax):
                            if(g_stitchingRoute_macro_count_sum > imageGather_basic.m_imagesCount and imageGather_basic.m_imageSelect == imageGather_basic.m_imageIDNext and g_isRecyclingMaterial == False):
                                return
                            elif(g_stitchingRoute_macro_count_sum > imageGather_basic.m_imagesCount and stitchingRouteCount == g_stitchingRoute_macro_count_sum and g_isRecyclingMaterial == True):
                                return
                            elif(g_stitchingRoute_macro_count_sum <= imageGather_basic.m_imagesCount and imageGather_basic.m_imageSelect == imageGather_basic.m_imageIDNext):
                                return
                            if (processID == 0):
                                imageGather_generated.Add(process(imageGather_basic.SelectAndRoll(),imageGather_basic.SelectAndRoll()))
                            elif(processID + 1 == processedIDMax):
                                if(isResize == True):
                                    imageGather_generated.CoverLast(process(imageGather_generated.SelectLast(), imageGather_basic.SelectAndRoll()).resize((stitchingRoute_micro_imageSize_width,stitchingRoute_micro_imageSize_height)))
                                else:
                                    imageGather_generated.CoverLast(process(imageGather_generated.SelectLast(),imageGather_basic.SelectAndRoll()))
                            else:
                                imageGather_generated.CoverLast(process(imageGather_generated.SelectLast(), imageGather_basic.SelectAndRoll()))
                            print("An image has been generated.")
                            stitchingRouteCount += 1
                            processedCount += 1
                            processID += 1
                        else:
                            break
                    if(processedCount >= stitchingRoute_micro_count):
                        break
                if(processedCount >= stitchingRoute_micro_count):
                    break
def RemoveDir(path):
    try:
        for file in os.listdir(path):
            os.remove(path + "\\" + file)
    except:
        pass
    os.rmdir(path)

def UI_bye():
    g.msgbox(
        "Does Automatic Image Stitcher facilitate your work?\nCould you star this project in Github or subscribe leoweyr on BiliBili?",
        SWNAME, "I would")
    webbrowser.open("https://github.com/leoweyr/Automatic_Image_Stitcher")
    webbrowser.open("https://space.bilibili.com/381580563")
    os._exit(0)

def main():
    global g_isRecyclingMaterial
    global g_stitchingRoute_macro_count_sum
    g.msgbox("Welcome to Automatic Image Stitcher!\nA graduation gift for WenHai.\nMade with ♥ by leoweyr.",SWNAME,"♥")
    while True:
        workFn = g.choicebox("What do you want me to do?",SWNAME,("Stitch images","Exit software"))
        if(workFn == "Stitch images"):
            while True:
                imageGatherPath_basic = g.diropenbox("Please select the folder that sores the images be stitched",SWNAME)
                if(imageGatherPath_basic == None):
                    while True:
                        notice = g.buttonbox("You haven't selected a folder!",SWNAME,["Reselect","Exit software"])
                        if(notice == "Reselect"):
                            break
                        elif(notice == "Exit software"):
                            UI_bye()
                if(len(os.listdir(imageGatherPath_basic)) == 0):
                    while True:
                        notice = g.buttonbox("Please select a folder with images!",SWNAME,["Reselect","Exit software"])
                        if (notice == "Reselect"):
                            break
                        elif (notice == "Exit software"):
                            UI_bye()
                files = os.listdir(imageGatherPath_basic)
                isAllImage = True
                for file in files:
                    try:
                        Image.open(imageGatherPath_basic + "\\" + file)
                    except:
                        isAllImage = False
                if(isAllImage == False):
                    while True:
                        notice = g.buttonbox("Please select a folder that contains only image type files, no other types of files can be in this folder!",SWNAME,["Reselect","Exit software"])
                        if (notice == "Reselect"):
                            break
                        elif (notice == "Exit software"):
                            UI_bye()
                imageGather_basic = ImageGather(imageGatherPath_basic)
                if(imageGather_basic.isGetNamedRule == False):
                    while True:
                        notice = g.buttonbox("Please let all images that be in the selected folder follow the named convention with serial number as the core!",SWNAME, ["Reselect", "Exit software"])
                        if (notice == "Reselect"):
                            break
                        elif (notice == "Exit software"):
                            UI_bye()
                else:
                    break
            imageGatherPath_generated = imageGatherPath_basic + "_generated"
            if(os.path.exists(imageGatherPath_generated) == True):
                RemoveDir(imageGatherPath_generated)
            os.mkdir(imageGatherPath_generated)
            imageGather_generated = ImageGather(imageGatherPath_generated)
            while True:
                stitchingRoute = g.enterbox("Please enter a splicing rule expression:",SWNAME,"( - ):*")
                g_stitchingRoute_macro_count_sum = 0
                isMicroCountThanMacroCount = False
                stitchingRoute_macro = stitchingRoute.split(",")
                for stitchingRoute_micro in stitchingRoute_macro:
                    try:
                        stitchingRoute_micro.split(")")[1]
                    except:
                        stitchingRoute_macro_count = imageGather_basic.m_imagesCount
                        g_stitchingRoute_macro_count_sum += stitchingRoute_macro_count
                    else:
                        stitchingRoute_macro_count = int(stitchingRoute_micro.split(")")[1].split(":")[0])
                        g_stitchingRoute_macro_count_sum += stitchingRoute_macro_count
                    try:
                        stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0].split("(")[1]
                    except:
                        stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0]
                    stitchingRoute_micro_count_sum = 0
                    for stitchingRoute_micro_each in stitchingRoute_micro_cycle.split("-"):
                        try:
                            stitchingRoute_micro_count_sum += int(stitchingRoute_micro_each[1:])
                        except:
                            stitchingRoute_micro_count_sum += 1
                    if(stitchingRoute_micro_count_sum > stitchingRoute_macro_count):
                        isMicroCountThanMacroCount = True
                if(g_stitchingRoute_macro_count_sum > imageGather_basic.m_imagesCount):
                    while True:
                        notice = g.buttonbox("The number of provided image materials to be processed is less than the <total number of images processed by the macro expression>. Do you want to recycle the provided image materials?",SWNAME,["Yes","No"])
                        if(notice == "Yes"):
                            g_isRecyclingMaterial = True
                            break
                        elif(notice == "No"):
                            g_isRecyclingMaterial = False
                            break
                elif(isMicroCountThanMacroCount == True):
                    while True:
                        notice = g.buttonbox("The sum of <number of pictures processed by micro-expression> cannot exceed <total number of pictures processed by macro-expression>!",SWNAME,["Reinput","Exit software"])
                        if(notice == "Reinput"):
                            break
                        elif(notice == "Exit software"):
                            UI_bye()
                #TODO: (Identify potential errors in micro-expression input: whether the <splicing method> parameter is 'V' or 'H')
                #TODO: (Identify potential errors in macro-expression input: whether the <the total number of pictures processed by the macro expression> parameter is int)
                #TODO: (Identify potential errors in macro-expression input: whether the <Optional: The width of the final generated image>*<Optional: The height of the final generated image> parameters are int and separated by "*")
                else:
                    break
            StitchImage(stitchingRoute,imageGather_basic,imageGather_generated)
            os.system("explorer.exe " + imageGatherPath_generated)
            while True:
                notice = g.buttonbox("The images are automatically stitched together in batches, and the corresponding folder has been opened for you.",SWNAME,["Stitch anothor images","Exit software"])
                if(notice == "Stitch anothor images"):
                    break
                elif(notice == "Exit software"):
                    UI_bye()
        elif(workFn == None or workFn == "Exit software"):
            UI_bye()

if __name__ == '__main__':
    main()