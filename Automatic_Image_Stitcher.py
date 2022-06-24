import os

from PIL import Image, ImageDraw
import easygui

class ImageGather:
    def __init__(self,path):
        self.m_path = path
        if(len(os.listdir(self.m_path)) == 0):
            self.m_imageIDFirst = 1
            self.m_imageIDNext = self.m_imageIDFirst
            self.m_imageSelect = self.m_imageIDFirst
        else:
            self.GetNamedRule()
            if (self.m_namedSerialization != 0 and self.m_imageIDFirst == 1):
                self.m_namedSerialization += 1
            if (self.m_imageIDFirst == 1):
                self.m_imageIDNext = imageNamesLen + 1
            elif (self.m_imageIDFirst == 0):
                self.m_imageIDNext = imageNamesLen
            self.m_imageSelect = self.m_imageIDFirst

    def GetNamedRule(self):
        imageNames = os.listdir(self.m_path)
        imageNamesLen = len(imageNames)
        if(imageNamesLen > 1):
            imageNames[0]
            imageNames[1]
            strID = 0
            while True:
                if(imageNames[0][strID] != imageNames[1][StrID]):
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
            while True:
                cheakPos_backup = cheakPos
                for imageName in imageNames:
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
                if(cheakPos == cheakPos_backup):
                    break
        else:
            strID = 0
            cheakMode = 0
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

    def SelectAndRoll(self):
        image = Image.open(self.m_path + "\\" + self.m_namedPrefix + str(self.m_imageSelect) + self.m_namedSuffix)
        self.m_imageSelectNext += 1
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
    stitchingRoute_macro = stitchingRoute.split(",")
    for stitchingRoute_micro in stitchingRoute_macro:
        stitchingRoute_micro_count = stitchingRoute_micro.split(")")[1]
        stitchingRoute_micro_cycle = stitchingRoute_micro.split(")")[0].split("(")[1]
        stitchingRoute_micro_cycle_each = stitchingRoute_micro_cycle.split("-")
        processedCount = 0
        while True:
            for processedUnit in stitchingRoute_micro_cycle_each:
                processedIDMax = int(processedUnit[1:])
                processID = 0
                if (processedUnit[0] == "V"):
                    process = StitchedImages_vertical
                elif (prcessUnit[0] == "H"):
                    process = StitchedImages_horizontal
                while True:
                    if(processedCount < stitchingRoute_micro_count or processID < processedIDMax):
                        if (processedID == 0):
                            imageGather_generated.Add(process(imageGather_basic.SelectAndRoll(),imageGather_basic.SelectAndRoll()))
                        elif(processID + 1 == processedIDMax):
                            imageGather_generated.CoverLast(process(imageGather_generated.SelectAndRoll(), imageGather_basic.SelectAndRoll()))
                        else:
                            imageGather_generated.CoverLast(process(imageGather_generated.SelectPresent(), imageGather_basic.SelectAndRoll()))
                        processedCount += 1
                        processID += 1
                    else:
                        break
                if(processedCount >= stitchingRoute_micro_count):
                    break
            if(processedCount >= stitchingRoute_micro_count):
                break

def main():
    return

if __name__ == '__main__':
    main()