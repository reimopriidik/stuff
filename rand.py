#!/usr/bin/env python
#-*- coding: utf-8 -*-
import string
import random
import csv
import timeit

start = timeit.default_timer()

size=2
chars=string.ascii_uppercase + string.digits
rows = 100000

with open('random2.csv', 'w') as csvfile:
	fieldnames = ['id', 'rand']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0, rows):		
		val = ''.join(random.choice(chars) for _ in range(size))
		writer.writerow({'id': i, 'rand': val})

print 'wrote ', rows, ' in ', round(timeit.default_timer() - start, 5), 's'