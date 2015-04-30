#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import csv, re
from collections import defaultdict

# from StringIO import StringIO
import json
import time, timeit
import pprint

pp = pprint.pprint

start = timeit.default_timer()

def createDict(): 
   return defaultdict(createDict)

validDelis = ['|',',',';','\t']

def findRowDelimiter(row):
   delimiter = None
   try:
      for c in row:
         if c in validDelis: delimiter = c
   finally:
      return delimiter

def findDelimiter(df):
   result = {}
   for index, row in df.iterrows():
      if len(row.values) == 1:
         for item in row.values:
            if findRowDelimiter(item):
               result['delimiter'] = findRowDelimiter(item)
               result['ingoreRows'] = index
               return result

def isAA(df):
   headers = df.columns.values.tolist()
   if 'Quantify Compound Summary Report ' in headers:
      if 'Printed' in df.loc[1].values[0]:
         fragments = []
         
         for index, row in df.iterrows():
            try:
               #Try to find item names with regex
               itemName = re.compile(r'Compound [0-9]+:  (.*)').findall(row.values[0])[0]
               fragments.append({
                  "start": index,
                  "item": itemName,
                  "end": None
                  })
            except Exception as e:
               pass
         
         result = createDict()
         for i, frag in enumerate(fragments):               
            try:
               if fragments[i+1]['start']:   
                  firstRow = fragments[i]['start']+3
                  lastRow = fragments[i+1]['start']-1
                  
                  dfFragment = df[firstRow:lastRow]
                  dfFragment.index = dfFragment[dfFragment.columns[0]]
                  dfFragment.columns = df[firstRow-1:lastRow].loc[firstRow-1].values
                  dfFragment.index.name = None
                  # dfFragment.drop(dfFragment.columns[3], 1)
                  result[frag['item']] = dfFragment
            except Exception, e:
               print e
               print i, fragments[i]['start'], '2ra mind 2ra unusta!'
         return result
   return False

def fixHeaders(df):
   headers = []
   for title in df.columns.values:
      if len(title.split(' ')) > 1:
         # headers.append((title.split(' ')[0], title.split(' ')[1]))
         headers.append(title.split(' ')[0])
      else:
         headers.append(title)
   if headers:
      return headers
   return False   

def stringToTime(val):
   time = 0
   try:
      if val.split(':'):
         for i, j in enumerate(val.split(':')):
            if j != '00':
               if i == 0:
                  time = time+float(j)
               elif i == 1:
                  time = time+float(j)/60
               elif i == 2:
                  time = time+float(j)/60/60
         return time
   except Exception, e:
      pass

def fixTime(timeRow):
   newRow = []
   for t in timeRow:
      try:
         newRow.append(float(t))
      except:
         newRow.append(stringToTime(t))
   return newRow

def openCSV(pathToFile, index = False):
   df = pd.read_csv(pathToFile) # error_bad_lines=False võib proovida
   notCSV = findDelimiter(df)
   if notCSV:
      if notCSV['ingoreRows']:
         df = pd.read_csv(pathToFile, skiprows=notCSV['ingoreRows']+1, sep=notCSV['delimiter'])
      elif notCSV['delimiter']:
         df = pd.read_csv(pathToFile, header = False, sep=notCSV['delimiter'])
   
   newHeaders = fixHeaders(df)
   if newHeaders:
      df.columns = newHeaders

   if isAA(df):
      df = isAA(df)
   elif index:
      if index.lower() in ['time', 'aeg']:
         df[index] = fixTime(df[index])

   return df

def merge(files, index):
   try:
      openFiles = []
      for f in files:
         openFiles.append(openCSV(f, index))
      df = openFiles[0].merge(openFiles[1], how='outer')
      for i, data in enumerate(openFiles):
         if i > 1:
            df = df.merge(openFiles[i], how='outer')
      return df
   except Exception, e:
      print e


# df1 = pd.read_csv('FECAL_IMC.final.an.unique_list.0.03.subsample_size5971.0.03.S5.2_10x-IMC10_35_48h_S5.2_10x.txt', skiprows=6, sep='\t')
# df2 = pd.read_csv('FECAL_IMC.final.an.unique_list.0.03.subsample_size5971.0.03.Sx.1_10x-IMC10_11_48h_Sx.1_10x.txt', skiprows=6, sep='\t')
# df1.merge(df2, how='outer', on="OTU", suffixes=('_fail1', '_fail2')).to_csv('result.csv')

obj1 = {}
obj2 = {}

with open('random.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for i, row in enumerate(reader):
      try:
         obj1[row['id']] = float(row['rand'])
      except Exception as e:
         obj1[row['id']] = 0

with open('random2.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for i, row in enumerate(reader):
      try:
         obj1[row['id']] = float(row['rand'])
      except Exception as e:
         obj1[row['id']] = 0
      


stop1 = timeit.default_timer()
print 'Python open CSV', round(stop1 - start, 5)


def f(x):
   try:
      obj1[x['id']] = float(x['rand'])
   except Exception as e:
      obj1[x['id']] = 0
   # obj1[x['id']] = x['rand']

df1 = pd.read_csv('random.csv')
df1.apply(f, axis=1)

df2 = pd.read_csv('random2.csv')
df2.apply(f, axis=1)

# print obj1

# df1.merge(df2, on="id", how='outer').to_csv('result_mil.csv')

stop2 = timeit.default_timer()
print 'Pandas open CSV', round(stop2 - stop1, 5)

# for i in range(0, 99):
#    df1 = openCSV('F201AA.csv', 'Time')
#    df2 = openCSV('EcoF207AASemi.csv', 'Time')
#    df3 = openCSV('F201Fermenterist.csv', 'Time')
#    df4 = openCSV('F201HPLC.csv', 'Time')

#    df1.merge(df2, how='outer').merge(df3, how='outer').merge(df4, how='outer')

# print pd.merge(df1, df2, how='outer')

# merge(['F201Fermenterist.csv', 'F201HPLC.csv', 'F201Biomass.csv', 'F201AA.csv'], 'Time')



#Get 5th row
#print asi1.loc[5].values[0]

#First 5 rows values
# for index, row in asi1.head(n=5).iterrows():
#  print row.values
