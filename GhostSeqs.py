#!/usr/bin/python

# Program to extract sequences from GHOST-
# online tunicates' database
# http://ghost.zool.kyoto-u.ac.jp/
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of last Modification - 04/08/2018

# [TODO]
#   1.  All the finding functions could be clubbed 
#       into a single function.

import urllib2
import re
import sys
from WriteDicts import DictWriter
from FileInfo import FileObject
from bs4 import BeautifulSoup

class GhostSeqsExtractor:

    def __init__(self):
        self.urlList = []
        self.namesSeqsDict = {"test":"anything"}
	self.baseUrl = "http://ghost.zool.kyoto-u.ac.jp/cgi-bin/fordetailkh21.cgi?name=%s&source=kh2013"
        self.genesAttrs = []
        print "Created"

    def addUrlsFromList(self, transcriptIdsList):
        for transcriptId in transcriptIdsList:
            url = self._constructUrl(transcriptId.replace("\n",""))
            self.urlList.append(url)

    def addUrlsFromFile(self, fileObject):
        lines = self._readFile(fileObject.getName())
        transcriptIdCol = fileObject.getTranscriptIdCol()
        if fileObject.hasHeader():
            startFrom = 1
        else:
            startFrom = 0
        for line in lines[startFrom:]:
            transcriptId = self._getTranscriptId(line, transcriptIdCol)
            url = self._constructUrl(transcriptId.replace("\n",""))
            self.urlList.append(url)

    def _constructUrl(self, transcriptId):
        url = self.baseUrl % transcriptId
        return url

    def _readFile(self, filename):
        with open(filename, 'r') as fIn:
            lines = fIn.readlines()
        return lines

    def _getTranscriptId(self, line, colNum):
        details = line.split(',')
        transcriptId = details[colNum]
        return transcriptId

    def getSequences(self):
        for url in self.urlList:
            processedHtml = self._getProcessedHtmlObject(url)
            # trs - tags of Html elements with sequence information
            allTrs = self._findAllTrs(processedHtml)
            if self._exists(allTrs):
                header, rawSequence = self._getHeaderAndSequence(allTrs)
                processedSequence = self._processSequence(rawSequence)
                self.namesSeqsDict[header] = processedSequence
                print url
            else:
                print "Error found with the following URL:"
                print url

    def _getProcessedHtmlObject(self,url):
        ghostHtml = self._getHtmlFromUrl(url)
        soup = self._parseHtml(ghostHtml)
        processedHtml = self._findInSoup(soup)
        return processedHtml

    def _getHtmlFromUrl(self,url):
        return urllib2.urlopen(url)

    def _parseHtml(self,html):
        return BeautifulSoup(html,"lxml")

    def _findInSoup(self,soup):
        return soup.find("table",{"class","Table2"})

    def _findAllTrs(self,processedHtml):
        try:
            allTrs = processedHtml.find_all("tr")
        except AttributeError as e:
            return "None"
        return allTrs

    def _exists(self, allTrs):
        if allTrs != "None":
            return True
        else:
            return False

    def _getHeaderAndSequence(self, allTrs):
        nuclSeqTr = self._getNuclSeqTr(allTrs)
        p = self._findSeqInTr(nuclSeqTr)
        header, rawSequence = self._extractHeaderAndSequence(p)
        return header, rawSequence

    def _getNuclSeqTr(self, allTrs):
        # tr of interest is the one with the no variation, i.e., 4th
        nuclSeqTr = allTrs[1]
        return nuclSeqTr

    def _findSeqInTr(self, nuclSeqTr):
        # p tag contains the sequence
        p = nuclSeqTr.find("p",{"class":"Txtbox2"})
        return p

    def _extractHeaderAndSequence(self, p):
        seq = p.text.split("\n")
        header = seq[1].encode("utf-8")
        sequence = ("").join(strings.encode("utf-8") for strings in seq[2:])
        return header, sequence

    def _processSequence(self, rawSequence):
        # remove spaces
        processedSequence = rawSequence.replace(" ","")
        # replace all non-ATGC with N
        #processedSequence = re.sub(r"[^ATGCatgc]","N",processedSequence)
        processedSequence = processedSequence
        return processedSequence

    def write2File(self, outputFile, fileType="fasta"):
        # fileType will be used as extension 
        dc = DictWriter(outputFile+'.'+fileType, self.namesSeqsDict)
        if fileType == "fasta":
            dc.write2Fasta()
        elif fileType == "csv":
            dc.write2Csv()
        elif fileType == "xlsx":
            dc.write2Excel()
        else:
            print "Invalid File Type"

def main():
    # The output filename should not have extension
    # Instead, the file type argument is used as extension
    if len(sys.argv) < 3:
        print "Usage: ", sys.argv[0]," <input file name> <output file name>"
        quit()
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    gse = GhostSeqsExtractor()
    fo = FileObject(inputFile, transcriptIdCol = 0)
    gse.write2File(outputFile, fileType = "csv")
    gse.write2File(outputFile, fileType = "xlsx")
    gse.write2File(outputFile, fileType = "fasta")

if __name__ == '__main__':
    main()
