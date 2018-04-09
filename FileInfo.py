#!/usr/bin/python

# A class for information about files to be
# read. This could be extended to include 
# numerous input file types. For now, it 
# is only for csv files
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of Last Modification - 04/08/2018

class FileObject:
    def __init__(self, fileName, header=True, khIdCol=0, uniqueNameCol=1, lengthCol=2, transcriptIdCol = 3):
        self.fileName = fileName
        self.header = header
        self.khIdCol = khIdCol
        self.uniqueNameCol = uniqueNameCol
        self.lengthCol = lengthCol
        self.transcriptIdCol = transcriptIdCol

    def hasHeader(self):
        return self.header

    def getName(self):
        return self.fileName

    def getKhIdCol(self):
        return self.khIdCol

    def getUniqueNameCol(self):
        return self.uniqueNameCol

    def getLengthCol(self):
        return self.lengthCol

    def getTranscriptIdCol(self):
        return self.transcriptIdCol

    def setKhIdCol(self, khIdCol):
        self.khIdCol = khIdCol

    def setUniqueNameCol(self, uniqueNameCol):
        self.uniqueNameCol = uniqueNameCol

    def setLengthCol(self, lengthCol):
        self.lengthCol = lengthCol

    def setTranscriptIdCol(self, transcriptIdCol):
        self.transcriptIdCol = transcriptIdCol

def main():
    fileObject = FileObject("filename")
    print fileObject.getName()
    print fileObject.getLengthCol()
    print fileObject.getKhIdCol()
    print fileObject.getUniqueNameCol()

if __name__ == '__main__':
    main()
