#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for find S algorithm

import sys
import math

Usage = "Usage: python partA.py testFileName"

# only one parameters
if len(sys.argv) != 2:
    print(Usage)
    sys.exit();

# print size of X
X = 2 ** 9
print str(X)

# print size of C
C = 2 ** X
print str(int(math.ceil(math.log10(C))))

# print size of H
H = 3 ** 9 + 1
print str(H)

# open training data
try:
    f = open("9Cat-Train.labeled")
except IOError:
    print "cannot open file 9Cat-Train.labeled"
    sys.exit()

# write hypothesis to file
try:
    f1 = open("partA4.txt", "wb")
except IOError:
    print "cannot open file 9Cat-Train.labeled"
    sys.exit()

# Find S algorithm
hypothesis = ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
count = 0
for line in f:
    if count != 0 and count % 30 == 0:
        message = '\t'.join(hypothesis) + '\n'
        f1.write(message)
    line = line.rstrip()
    attributes = line.split('\t')
    if attributes[9].split(' ')[1] == 'low':
        count += 1
        continue
    for i in range(0, 9):
        attribute = attributes[i].split(' ')
        if attribute[1] == hypothesis[i]:
            continue
        elif hypothesis[i] == 'null':
            hypothesis[i] = attribute[1]
        else:
            hypothesis[i] = '?'
    count += 1

if count != 0 and count % 30 == 0:
    message = '\t'.join(hypothesis) + '\n'
    f1.write(message)

f.close()
f1.close()

# open dev data, test mis classification rate
try:
    f = open("9Cat-Dev.labeled")
except IOError:
    print "cannot open file 9Cat-Dev.labeled"
    sys.exit()
count = 0
wrong = 0
for line in f:
    count += 1
    line = line.rstrip()
    attributes = line.split('\t')
    dif = 0
    for i in range(0, 9):
        if hypothesis[i] == '?' or hypothesis[i] == attributes[i].split(' ')[1]:
            continue
        else:
            dif += 1
    if attributes[9].split(" ")[1] == 'high':
        if dif != 0:
            wrong += 1
    else:
        if dif == 0:
            wrong += 1
print float(wrong) / float(count)
f.close()


# open test data, predict result
try:
    f = open(sys.argv[1])
except IOError:
    print "cannot open file" + sys.argv[1]
    sys.exit()

for line in f:
    line = line.rstrip()
    attributes = line.split('\t')
    dif = 0
    isHigh = 1
    for i in range(0, 9):
        attribute = attributes[i].split(" ")
        if hypothesis[i] == '?' or hypothesis[i] == attribute[1]:
            continue
        else:
            isHigh = 0
            break
    if isHigh == 1:
        print "high"
    else:
        print "low"

f.close()
