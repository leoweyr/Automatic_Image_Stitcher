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
        if(self.m_imagesCount == 0):
            self.m_imageIDFirst = 1
            self.m_imageIDNext = self.m_imageIDFirst
            self.m_imageSelect = self.m_imageIDFirst
        else:
            if(self.GetNamedRule() == False):
                return False
            else:
                if (self.m_namedSerialization != 0 and self.m_imageIDFirst == 1):
                    self.m_namedSerialization += 1
                if (self.m_imageIDFirst == 1):
                    self.m_imageIDNext = imageNamesLen + 1
                elif (self.m_imageIDFirst == 0):
                    self.m_imageIDNext = imageNamesLen
                self.m_imageSelect = self.m_imageIDFirst

    def GetNamedRule(self):
        if(self.m_imagesCount > 1):
            imageNames[0]
            imageNames[1]
            strID = 0
            while True:
                if(imageNames[0][strID] != imageNames[1][StrID]):
                    try:
                        int(imageNames[0][strID])
                        int(imageNames[1][strID])
                    except:
                        return False
                    differentPos = strID
                    break
                strID += 1
            if(differentPos == 0):
                self.m_namedPrefix = ""
            else:
                self.m_namedPrefix = imageNames[0][0:differentPos-1]
            self.m_namedSerialization = 0
            cheakPos = differentPos
            isGetNamedSuffix = False
            intCount = 0
            while True:
                cheakPos_backup = cheakPos
                for imageName in imageNames:
                    try:
                        int(imageName)
                    except:
                        pass
                    else:
                        intCount += 1
                    if(imageName[cheakPos] == "1" and isGetNamedSuffix == False):
                        self.m_namedSuffix = imageNames[cheakPos+1:]
                        isGetNamedSuffix = True
                    if(imageName[cheakPos] == "0"):
                        try:
                            int(imageName[cheakPos + 1])
                        except:
                            self.m_imageIDFirst = 0
                            break
                        else:
                            self.m_namedSerialization += 1
                            cheakPos += 1
                            break
                if(intCount == 0):
                    return False
                if(cheakPos == cheakPos_backup):
                    break
        else:
            strID = 0
            cheakMode = 0
            intCount = 0
            self.m_namedSerialization = 0
            for word in imageNames[0]:
                try:
                    int(word)
                except:
                    if(cheakMode == 1 and isLastZero == True):
                        self.m_imageIDFirst = 0
                    if(cheakMode == 1):
                        self.m_namedSuffix = imageNames[0][strID]
                else:
                    intCount += 1
                    if(cheakMode == 0 and strID != 0):
                        self.m_namedPrefix = imageNames[0][strID - 1]
                        cheakMode += 1
                    elif(cheakMode == 0 and strID == 0):
                        self.m_namedPrefix = ""
                        cheakMode += 1
                    elif(cheakMode == 1 and isLastZero == True):
                        self.m_namedSerialization += 1
                    elif(cheakMode == 1 and word == "0"):
                        isLastZero = True
                strID += 1
            if(intCount == 0):
                return False
        return True

    def Add(self,image):
        image.save(self.m_path + "\\" + self.m_namedPrefix + str(self.m_imageIDNext) + self.m_namedSuffix)
        self.m_imageIDNext += 1

    def CoverLast(self,image):
        image.save(self.m_path + "\\" + self.m_namedPrefix + str(self.m_imageIDNext - 1) + self.m_namedSuffix)

    def SelectReset(self):
        self.m_imageSelect = self.m_imageIDFirst

    def SelectPresent(self):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + str(self.m_imageSelect) + self.m_namedSuffix)
        return image

    def SelectAndRoll(self,isSelectLoop=g_isRecyclingMaterial):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + str(self.m_imageSelect) + self.m_namedSuffix)
        self.m_imageSelect += 1
        if(isSelectLoop == True and self.m_imageSelect == self.m_imageIDNext):
            self.SelectReset()
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


def StitchImage(stitchingRoute,imageGather_basic,imageGather_generated): #(H4)50:280*502
    global g_isRecyclingMaterial
    global g_stitchingRoute_macro_count_sum
    imageGather_generated.m_namedPrefix = imageGather_basic.m_namedPrefix
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
                stitchingRoute_micro_count = stitchingRoute_micro.split(")")[1].split(":")[0]
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
                            if (processedID == 0):
                                imageGather_generated.Add(process(imageGather_basic.SelectAndRoll(),imageGather_basic.SelectAndRoll()))
                            elif(processID + 1 == processedIDMax):
                                if(isResize == True):
                                    imageGather_generated.CoverLast(process(imageGather_generated.SelectAndRoll(), imageGather_basic.SelectAndRoll()).resize((stitchingRoute_micro_imageSize_width,stitchingRoute_micro_imageSize_height)))
                                else:
                                    imageGather_generated.CoverLast(process(imageGather_generated.SelectAndRoll(),imageGather_basic.SelectAndRoll()))
                            else:
                                imageGather_generated.CoverLast(process(imageGather_generated.SelectPresent(), imageGather_basic.SelectAndRoll()))
                            stitchingRouteCount += 1
                            processedCount += 1
                            processID += 1
                        else:
                            break
                    if(processedCount >= stitchingRoute_micro_count):
                        break
                if(processedCount >= stitchingRoute_micro_count):
                    break

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
        if(workFn == "Stitch image"):
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
                if(imageGather_basic == False):
                    while True:
                        notice = g.buttonbox("Please let all images that be in the selected folder follow the named convention with serial number as the core!",SWNAME, ["Reselect", "Exit software"])
                        if (notice == "Reselect"):
                            break
                        elif (notice == "Exit software"):
                            UI_bye()
                break
            imageGatherPath_generated = imageGatherPath_basic + "_generated"
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
                        stitchingRoute_macro_count = stitchingRoute_micro.split(")")[1].split(":")[0]
                        g_stitchingRoute_macro_count_sum += stitchingRoute_macro_count
                    try:
                        stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0].split("(")[1]
                    except:
                        stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0]
                    stitchingRoute_micro_count_sum = 0
                    for stitchingRoute_micro_each in stitchingRoute_micro_cycle.split("-"):
                        stitchingRoute_micro_count_sum += int(stitchingRoute_micro_each[1:])
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
            while True:
                notice = g.buttonbox("The images are automatically stitched together in batches, and the corresponding folder has been opened for you.",SWNAME,["Stitch anothor images","Exit software"])
                os.system("explorer.exe " + imageGatherPath_generated)
                if(notice == "Stitch anothor images"):
                    break
                elif(notice == "Exit software"):
                    UI_bye()
        elif(workFn == None or workFn == "Exit software"):
            UI_bye()

if __name__ == '__main__':
    main()