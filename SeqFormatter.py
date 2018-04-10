#!/usr/bin/python

# Program to format sequences retreived from 
# GHOST database. Sometimes, when designing primers
# for sequencing or synthesizing sequences themselves,
# one needs to modify to the sequence so that the 
# libraries can be prepared and identified.
# This class does that formatting.
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of Last Modification - 04/09/2018

import sys
import re
from FileInfo import FileObject
from WriteDicts import DictWriter

class SeqFormatter:
    def __init__(self):
        self.namesSeqsDict = {}
        self.formattingParameters = {'minSeqLength':500,
                                    'trimStartBy':200,
                                    'trimEndBy':200,
                                    'beginFlankSeq':"gcggccgc",
                                    'endFlankSeq':"gaattCCCTATAGTGAGTCGTATTA"}
        self.formattedSeqsDict = {}

    def getFormattingParameters(self):
        for parameter, value in self.formattingParameters.iteritems():
            print parameter, "\t", value

    def setFormattingParameters(self, **kwargs):
        parameters = self.formattingParameters.keys()
        for key, value in kwargs.iteritems():
            if key in parameters:
                self.formattingParameters[key] = value
            else:
                print "WARNING: Invalid Key: ", key

    def readSeqsFromFasta(self, inputFile):
        lines = self.returnFileLines(inputFile)
        for ind, line in enumerate(lines):
            if self.isHeader(line):
                header = line
                seqInd = ind+1
                sequence = lines[seqInd]
            self.namesSeqsDict[header] = sequence

    def returnFileLines(self, filename):
        with open(filename,'r') as fIn:
            lines = fIn.readlines()
        return [line.strip() for line in lines]

    def isHeader(self,line):
        matchObj = re.match(r'^>.*',line)
        if matchObj:
            return True
        else:
            return False

    def readSeqsFromCsv(self, inputFile, sep=','):
        lines = self.returnFileLines(inputFile)
        for line in lines:
            header, sequence = line.split(sep)
            self.namesSeqsDict[header] = sequence

    def formatSeqs(self):
        for header, sequence in self.namesSeqsDict.iteritems():
            if self.isSmall(sequence):
                formattedSequence = sequence
            else:
                formattedSequence = self.trimAndAppendFlanks(sequence)
            self.formattedSeqsDict[header] = formattedSequence

    def isSmall(self, sequence):
        minLength = self.formattingParameters['minSeqLength']
        if len(sequence) < minLength:
            return True
        else:
            return False

    def trimAndAppendFlanks(self, sequence):
        beginFlankSeq = self.formattingParameters['beginFlankSeq']
        endFlankSeq = self.formattingParameters['endFlankSeq']
        trimStartBy = self.formattingParameters['trimStartBy']
        trimEndBy = self.formattingParameters['trimEndBy']
        seqLength = len(sequence)
        trimmedSeq = sequence[trimStartBy:seqLength-trimEndBy]
        appendedSeq = beginFlankSeq + trimmedSeq + endFlankSeq
        return appendedSeq

    def write2File(self, outputFile, fileType="fasta"):
        # fileType will be used as extension 
        dc = DictWriter(outputFile+'.'+fileType, self.formattedSeqsDict)
        if fileType == "fasta":
            dc.write2Fasta()
        elif fileType == "csv":
            dc.write2Csv()
        elif fileType == "xlsx":
            dc.write2Excel()
        else:
            print "Invalid File Type"

    def getFormattedSeqs(self):
        # returns a dictionary of sequence names as keys
        # and sequences as values
        # can be used for writing to different file types
        return self.formattedSeqsDict


def main():
    if len(sys.argv) < 2:
        print "Usage: ./" + sys.argv[0] + "<input file name>"
        quit()
    filename = sys.argv[1]
    sf = SeqFormatter()
    sf.readSeqsFromFasta(filename)
    #sf.readSeqsFromCsv(filename, sep="\t")
    sf.getFormattingParameters()
    sf.formatSeqs()
    sf.write2File("formattedSeqs",fileType="xlsx")


if __name__ == '__main__':
    main()


