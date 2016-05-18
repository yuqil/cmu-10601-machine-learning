#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for warm up in decision tree.

import sys
import math

Usage = "Usage: python partA.py training data, dev data"


def cal_entropy(pos, neg):
    total = pos + neg
    p_pos = float(pos) / total
    p_neg = float(neg) / total
    etp = p_pos * math.log(1 / float(p_pos), 2) + p_neg * math.log(1 / float(p_neg), 2)
    return etp


# only one parameters
if len(sys.argv) != 2:
    print(Usage)
    sys.exit();

# open training data
try:
    training = open(sys.argv[1])
except IOError:
    print "cannot open training data"
    sys.exit()

# open develop data
try:
    dev = open(sys.argv[1])
except IOError:
    print "cannot open develop data"
    sys.exit()


# read training data
dict = {}
positive = 0
negative = 0
training.readline()
index = 0
for line in training:
    line = line.rstrip()
    attributes = line.split(',')
    if not dict.__contains__(attributes[-1]):
        dict[attributes[-1]] = 0
    dict[attributes[-1]] = (dict.get(attributes[-1]) + 1)

list = dict.values()
positive = list[0]
negative = list[1]

# calculate entropy
entropy = cal_entropy(positive, negative)
print "entropy: " + str(entropy)
training.close()

# test develop data
keys = dict.keys()
max = 0
majority = ""
for key in keys:
    if dict.get(key) > max:
        majority = key
        max = dict.get(key)

error = 0
size = 0
dev.readline()
for line in dev:
    size += 1
    line = line.rstrip()
    attributes = line.split(",")
    if attributes[-1] != majority:
        error += 1
dev.close()

print "error: " + str(float(error) / size)
