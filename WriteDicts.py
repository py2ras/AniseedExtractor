#!/usr/bin/python

# Class to write dictionary objects to files.
# We commonly encounter inputs and outputs as
# named sequences. These are best stored as 
# dictionaries. This class is to write such
# dictionaries to output files.
# @author - Sarthak Sharma <sarthaksharma@gatech.edu>
# Date of Last Modification - 04/10/2018

import sys
import xlsxwriter

class DictWriter:
    def __init__(self, outputFile, outDict):
        self.outputFile = outputFile
        self.outDict = outDict

    def write2Fasta(self):
        outputFile = self.outputFile
        with open(outputFile,'w') as fOut:
            for header, sequence in self.outDict.iteritems():
                fOut.write(header)
                fOut.write("\n")
                fOut.write(sequence)
                fOut.write("\n")

    def write2Excel(self):
        outputFile = self.outputFile
        workbook = xlsxwriter.Workbook(outputFile)
        worksheet = workbook.add_worksheet()
        headerCol0 = "Sequence Name"
        headerCol1 = "Sequence"
        worksheet.write(0,0,headerCol0)
        worksheet.write(0,1,headerCol1)
        rowNum = 1
        for header, sequence in self.outDict.iteritems():
            worksheet.write(rowNum,0,header.replace("\n","").replace(">",""))
            worksheet.write(rowNum,1,sequence.replace("\n",""))
            rowNum = rowNum + 1
        workbook.close()

    def write2Csv(self, sep = ","):
        outputFile = self.outputFile
        with open(outputFile,'w') as fOut:
            fOut.write("Sequence Name" + sep + "Sequence\n")
            for header, sequence in self.outDict.iteritems():
                fOut.write(header + sep + sequence)
                fOut.write("\n")
