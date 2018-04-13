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
        self.formattingParameters = {
                                    'minLength':500,
                                    'trimStartBy':0,
                                    'trimEndBy':200,
                                    'beginFlankSeq':"gcggccgc",
                                    'endFlankSeq':"gaattCCCTATAGTGAGTCGTATTA",
                                    'requiredSeqLength':500
                                    }
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
                print header.replace('>','') + " is smaller than the minLength"
                formattedSequence = sequence
            else:
                formattedSequence = self._formatSeq(sequence)
            self.formattedSeqsDict[header] = formattedSequence

    def isSmall(self, sequence):
        minLength = self.formattingParameters['minLength']
        if len(sequence) < minLength:
            return True
        else:
            return False

    def _formatSeq(self,sequence):
        trimmedSeq = self._trimSeq(sequence)
        appendedSeq = self._appendFlanks(trimmedSeq)
        return appendedSeq

    def _trimSeq(self,sequence):
        trimEndBy = self.formattingParameters['trimEndBy']
        requiredSeqLength = self.formattingParameters['requiredSeqLength']
        if len(sequence) < (requiredSeqLength + trimEndBy):
            trimmedSeq = sequence[0:requiredSeqLength]
        else:
            trimmedSeq = sequence[-(requiredSeqLength + trimEndBy):-trimEndBy]
        return trimmedSeq

    def _appendFlanks(self, sequence):
        beginFlankSeq = self.formattingParameters['beginFlankSeq']
        endFlankSeq = self.formattingParameters['endFlankSeq']
        appendedSeq = beginFlankSeq + sequence + endFlankSeq
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
    sf.write2File("formattedSeqs",fileType="csv")


if __name__ == '__main__':
    main()


