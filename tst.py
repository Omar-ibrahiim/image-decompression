import io
from PyQt5.QtGui import *##QPixmap
from PIL import Image,ImageQt
from PyQt5 import QtWidgets, QtCore,QtGui


def getData():
    # get the file and read it
    filePath= QtWidgets.QFileDialog.getOpenFileName(None,  'load', "./","All Files *;;" "*.jpg;;" "*.jpeg")
    #getting the filename indexes in the filepath#
    BegOfTheName= filePath[0].rfind('/')+1 
    LastOfTheName= filePath[0].rfind('.')
    filename=filePath[0][BegOfTheName:LastOfTheName] 
    datatype = filePath[0][LastOfTheName+1:] #get the datatype from the filePath
    #making sure of the file type and read it#
    if(datatype=="jpg" or datatype=="jpeg"):
        
        fileOpened = open(filePath[0],"rb")
        #reading the whole file as bin
        data=fileOpened.read()
        fileOpened.close()
    
    else:
        return None,None
    return [data,filename]



def getChunkesFromImage(allBin):

    FF =b'\xff'
    SOI=b'\xd8'
    APP=b'\xe0'
    SOS=b'\xda'
    EOI=b'\xd9'
    
    #getStartsOfChunks(allBin)
    StartOfChunks=[]
    prevByte=None
    for index,byte in enumerate(allBin):
        if byte.to_bytes(1,"little") == SOS and prevByte.to_bytes(1,"little")==FF:
            StartOfChunks.append(index)
        prevByte=byte
    #print(StartOfChunks)

    #getChunks(allBin,StartOfChunks)
    Chunk_counter=len(StartOfChunks)-1
    Chunks=[None]*Chunk_counter
    for indexOfChunk,indexOfChunkStart in enumerate(StartOfChunks):
        if indexOfChunk >=Chunk_counter:
            break
        indexOfChunkEnd=StartOfChunks[indexOfChunk+1]
        lastChunkEndindex=StartOfChunks[-1]
        Chunks[indexOfChunk]=allBin[:indexOfChunkEnd]+allBin[lastChunkEndindex:]
        # if indexOfChunk==0:
        #     Chunks[indexOfChunk]=allBin[:indexOfChunkEnd]+EOI
        # else:
        #     # Chunks[indexOfChunk]=Chunks[indexOfChunk-1][:-1]+SOS+allBin[indexOfChunkStart+1:indexOfChunkEnd]+EOI
        #     Chunks[indexOfChunk]=allBin[:indexOfChunkEnd]+EOI

    return Chunks,Chunk_counter

#Chunks,numberOfChunks,image = getChunkesFromImage(data)
def getPicturesFromChunks(Chunks):
    pictures=[]
    for Chunk in Chunks:
        try:
            f = io.BytesIO(Chunk)
            picture = Image.open(f)
            pictures.append(picture)
        except :
            pictures.append(None)
    return pictures


def getPixmapsFromPictures(pictures):
    pixmaps=[]
    for picture in pictures:
        if picture is None :
            pixmaps.append(None)
        else:
            pixmaps.append(QPixmap(ImageQt.toqpixmap( picture)))
    return pixmaps