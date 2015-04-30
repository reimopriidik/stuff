import csv, re
import os, sys, glob

from collections import defaultdict
#Helps to create nested dictionaries
def createDict():   
    return defaultdict(createDict)

def isNumber(val):
    try:
        float(val)
        return True
    except:
        return False

# Find txt files in dir
txtFileList = []
for txtFile in glob.glob("*.txt"):
    txtFileList.append(txtFile)

# Ask filename
if len(txtFileList) == 1:
    userInput = input('Open "'+txtFileList[0]+'"? [Enter,Y/N] \n')
    if not userInput or userInput.lower() in ['y', 'yes', 'j', 'jah', 'ja']:
        pathToFile = txtFileList[0]
    else:
        sys.exit('\nAborting. Move correct TXT file to this folder and run me again.')
elif len(txtFileList) > 1:
    print('Please choose input file:')
    for i, f in enumerate(txtFileList):
        print(str(i+1)+' - '+f)
    userInput = input('\nSelect file: enter 1-'+str(len(txtFileList))+'\n')
    try:
        pathToFile = txtFileList[int(userInput)-1]
    except Exception as e:
        sys.exit('\nAborting. Wrong user input. Run me again to start over.')
else:
    sys.exit('No *.txt file in dir.\nPlease copy "input.txt" file to this folder.')

#Define vars
result = {}
result['data'] = {}
result['headers'] = []

#Define group seperator
regexp = re.compile(r'Compound [0-9]+: ')

#Open and read file
with open(pathToFile, 'r') as f:
    print('Opened ', pathToFile)
    reader = csv.reader(f, delimiter='\t')

    for row in reader:
        try:
            if 'Name' in row and 'Response' in row:
                result['columns'] = row
                nameIndex = row.index('Name')
            elif 'Printed' in row[0]:
                result['date'] = row[0]
            if regexp.search(row[0]) is not None:
                rowName = str(row[0].split(' ')[3]+' '+row[0].split(' ')[4])
                result['data'][rowName] = []
                result['headers'].append(rowName)
            if isNumber(row[0]):
                result['data'][rowName].append(row)
            if regexp.search(row[0]) is not None:
                continue
        except Exception as e:
            pass

# Kuskil on parem lahendus
sampleList = [] 
for k,v in result['data'].items():
    for i in v:
        if i[nameIndex] not in sampleList:
            sampleList.append(i[nameIndex])

#Build CSV data
i = 1
iHolder = {}
for colNr, col in enumerate(result['columns']):
    if col.lower() not in ['', 'name']:
        print(str(i)+' - '+col)
        iHolder[i] = colNr
        i += 1
userInput = input('\nPlease enter column number\n')

# Ask col name
try:
    useCol = int(iHolder[int(userInput)])
    print('Using "'+result['columns'][iHolder[int(userInput)]]+'"')
except Exception as e:
    sys.exit('\nAborting. Wrong user input. Run me again to start over.')

csvData = createDict()
for item in sorted(result['headers']):
    for sample in sampleList:
        for row in result['data'][item]:
            if sample in row:
                csvData[sample]['Sample name'] = sample
                csvData[sample][item] = row[useCol]
result['headers'].insert(0, 'Sample name')

#Write to csv
print('Writing data to CSV')
#generate csv name
outputFile = pathToFile.split('.')[0]+'_'+re.sub(r'[^\w]', '', result['columns'][iHolder[int(userInput)]])+'.csv'
with open(outputFile,'w', newline='') as csfFile:
    dw = csv.DictWriter(csfFile, delimiter=',', fieldnames=result['headers'])
    dw.writeheader()
    for row in sorted(csvData):
        dw.writerow(csvData[row])
print('Writing CSV done, file "'+outputFile+'" created. Have a nice day.')
