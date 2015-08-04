#!/usr/bin/env python
#-*- coding: utf-8 -*-
import string
import random
import csv
import timeit

start = timeit.default_timer()

columns = 2 #Number of columns (1-3)
rows = 1000 #Number of rows 
size = 10 #Data length in row

if columns == 1:
	fileName = 'rand'+str(rows)+','+str(size)+'.csv'
elif columns == 2:
	fileName = 'rand'+str(rows)+','+str(size)+',2cols'+'.csv'
elif columns == 3:
	fileName = 'rand'+str(rows)+','+str(size)+',3cols'+'.csv'

chars=string.ascii_uppercase + string.digits
with open(fileName, 'w') as csvfile:
	if columns == 1:
		fieldnames = ['id', 'rand']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(0, rows):		
			val = ''.join(random.choice(chars) for _ in range(size))
			writer.writerow({'id': i, 'rand': val})
	elif columns == 2:
		fieldnames = ['id', 'rand1', 'rand2']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(0, rows):		
			val1 = ''.join(random.choice(chars) for _ in range(size))
			val2 = ''.join(random.choice(chars) for _ in range(size))
			writer.writerow({'id': i, 'rand1': val1, 'rand2': val2})
	elif columns == 3:
		fieldnames = ['id', 'rand1', 'rand2', 'rand3']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(0, rows):		
			val1 = ''.join(random.choice(chars) for _ in range(size))
			val2 = ''.join(random.choice(chars) for _ in range(size))
			val3 = ''.join(random.choice(chars) for _ in range(size))
			writer.writerow({'id': i, 'rand1': val1, 'rand2': val2, 'rand3': val3})

print 'wrote', size, 'characters in', rows, 'rows\nin', columns, 'columns in',\
round(timeit.default_timer() - start, 5), 'seconds',
