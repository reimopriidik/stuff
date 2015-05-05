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
   # writeRowCsv(merged)
   writeDictCsv(merged)

def writeDictCsv(merged):
   result = {}
   
   for otu in merged:
      result[otu] = {}

   for i, header in enumerate(merged['headers']):
      for otu in merged:
         try:
            if otu:
               result[otu][header] = merged[otu][i]
         except Exception as e:
            pass

   with open('dictWriter.csv', 'w') as csvfile:
      fieldnames = sorted(merged['headers'])
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for k in sorted(result):
         writer.writerow(result[k])

def writeRowCsv(merged):
   # merged = rowsToDict(merged)
   with open('merged.csv', 'wb') as csvfile:
      csvWriter = csv.writer(csvfile)
      csvWriter.writerow(merged['headers'])
      for k in sorted(merged):
         if k != 'headers' and merged[k]:
            csvWriter.writerow(merged[k])

if __name__ == '__main__':
   import os, sys, glob
   import timeit
   timerStart = timeit.default_timer()
   
   files = []

   try:
      #Get all .txt files in working dir
      for txtFile in glob.glob("*.txt"):
         files.append(txtFile)   
      mergeFecFiles(files)
   except Exception, e:
      print 'Could not open files in dir. Exception: ', e
   finally:
      timerStop = timeit.default_timer()
      if files:
         for i, f in enumerate(files):
            print i+1, ' - ', f
         print i+1, 'files merged in ', round(timerStop - timerStart, 3), 's'

