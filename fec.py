#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

def readFecFiles(files):
   result = {}
   for f in files:
      fileId = f.split('-')[1].replace('.txt', '')
      result[fileId] = {}
      with open(f) as csvfile:
         for i, row in enumerate(csvfile):
            splitRow = row.replace('\r\n', '').split('\t')
            if i == 6: result[fileId]['headers'] = [header+'_'+fileId for header in splitRow]
            if i > 6: result[fileId][splitRow[0]] = splitRow
   return result

def mergeFecFiles(files):
   merged = {}
   files = readFecFiles(files)
   for f, data in files.items():
      for k, v in data.items():
         merged[k] = []
   for f, data in files.items():
      for k, v in data.items():
         if v: 
            merged[k].extend(v)
   
   writeMergedCsv(merged)

def writeMergedCsv(merged):
   with open('merged.csv', 'r+') as csvfile:
      csvWriter = csv.writer(csvfile, lineterminator='\n')
      csvWriter.writerow(merged['headers'])
      for k in sorted(merged):
         if k != 'headers' and merged[k]:
            csvWriter.writerow(merged[k])

if __name__ == '__main__':
   import os, sys, glob
   import timeit
   timerStart = timeit.default_timer()
   
   files = []
   #Define files
   # files = [
   #    'files/FECAL_IMC.final.an.unique_list.0.03.subsample_size5971.0.03.Sx.1_10x-IMC10_11_48h_Sx.1_10x.txt',
   #    'files/FECAL_IMC.final.an.unique_list.0.03.subsample_size5971.0.03.S5.2_10x-IMC10_35_48h_S5.2_10x.txt', 
   #    'files/FECAL_IMC.final.an.unique_list.0.03.subsample_size5971.0.03.S3.1_10x-IMC10_21_48h_S3.1_10x.txt'
   # ]

   try:
      #Get all .txt files in working dir
      for txtFile in glob.glob("*.txt"):
         files.append(txtFile)   
      mergeFecFiles(files)
   except Exception, e:
      print 'Failed to run', e
   finally:
      timerStop = timeit.default_timer()
      if files:
         for i, f in enumerate(files):
            print i+1, ' - ', f
         print i+1, 'files merged in ', round(timerStop - timerStart, 3), 's'