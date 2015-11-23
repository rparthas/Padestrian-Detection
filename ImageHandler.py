# -*- coding: utf-8 -*-
"""

@author: Ankit Singh
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from HistogramProcessing import HistogramOperations
import os

class Imagehandler(object):
    def __init__(self,path):
        if (os.path.exists(path) and os.path.isfile(path)):
            self.ImagePath=path
            self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        else:
            print "file not found"
    
    def __convertImagetoBlackWhite(self):
        self.Image=cv.imread(self.ImagePath,cv.IMREAD_COLOR)
        self.imageOriginal=self.Image
        if(self.Image is None):
            print "some problem with the image"
        else:
            print "Image Loaded"
            
        self.Image=cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
        self.Image=cv.adaptiveThreshold(self.Image,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
        return self.Image
    
    def WritingImage(self,image,path,imageName):
        if(image is None):
            print"Image is not valid.Please select some other image"
        else:
            image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
            print path+imageName
            cv.imwrite(path+imageName,image)
            cv.imshow(imageName,image)
            cv.waitKey(0);


    
    def ImagesToTiles(self,tileX,tileY):
        imageHeight,imageWidth=self.Image.shape[:2]
        imageHeight=int(imageHeight/tileY)*tileY
        imageWidth=int(imageWidth/tileX)*tileX
        self.Image = cv.resize(self.Image,(imageWidth,imageHeight), interpolation = cv.INTER_CUBIC)
        #cv.resize takes shape as (width,height) instead of height,width
        i=0
        j=0
        featureVector=[]
        print imageHeight
        print imageWidth
        count=0
        while i< imageHeight:
            j=0
            while j < imageWidth:
                img=self.Image[j:j+tileY,i:i+tileX]
                if len(img)==0:
                    continue
#                cv.rectangle(self.Image,(j,i), (j+tileY,i+tileX), (0,255,0),3)
                subTilesList=self.SubDivideTile(img,4,4)
#                print subTilesList
                histogramSubTiles=[]
#                    print subTilesList
                for tile in subTilesList:
#                    print tile
                    count +=1
                    tileObj=HistogramOperations(tile)
                    akrusd=tileObj.HistogramOfGradient(tile,9)
                    histogramSubTiles.append(akrusd)
                featureVector.append(tileObj.ConcatAndNormalisationofHistogram(histogramSubTiles))  
#                print featureVector
                print count
                j=j+tileY
            i=i+tileX
        #image should be shown at last as image is changed after every rectangle,square,cirlce operation
#        cv.imshow("hi",self.Image)
#        cv.waitKey(0)
#        except:
#            print featureVector
        print "DONE"
        return featureVector
        
    def SubDivideTile(self,inputTile,tileX,tileY):
        #print inputTile
        imageHeight,imageWidth=inputTile.shape[:2]
        imageHeight=int(imageHeight/tileY)*tileY
        imageWidth=int(imageWidth/tileX)*tileX
        try:
            tile = cv.resize(inputTile,(imageWidth,imageHeight), interpolation = cv.INTER_CUBIC)
        except:
            print inputTile
            return
        subTilesList=[]
        i=0
        j=0
        #count=1
        while i< imageHeight:
            j=0
            while j < imageWidth:
                img=tile[j:j+tileY,i:i+tileX]
                subTilesList.append(img)
                cv.rectangle(self.Image,(j,i), (j+tileY,i+tileX), (255,0,0),3)
               # print img
                j=j+tileY

#                count +=1
            i=i+tileX
       # print "adasdadadadadadas",count)
        return subTilesList   
    

        
    
        