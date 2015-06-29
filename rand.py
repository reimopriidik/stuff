#!/usr/bin/env python
#-*- coding: utf-8 -*-
import string
import random
import csv
import timeit

start = timeit.default_timer()

rows = 100000 #Number of rows 
size = 5 #Data length in row
fileName = 'rand.csv'

chars=string.ascii_uppercase + string.digits
with open(fileName, 'w') as csvfile:
	fieldnames = ['id', 'rand']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0, rows):		
		val = ''.join(random.choice(chars) for _ in range(size))
		writer.writerow({'id': i, 'rand': val})

print 'wrote ', rows, ' in ', round(timeit.default_timer() - start, 5), 's'
