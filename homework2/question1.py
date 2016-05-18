#!/usr/bin/python

# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for splitting the text

import string
import sys

Usage = "Usage: python question1.py 'path/to/input/'"

# two parameters
if (len(sys.argv) != 2):
    print(Usage)

# open input file
try:
    f = open(sys.argv[1])
except IOError:
    print "cannot open file" + sys.argv[1]
    sys.exit()

# set use remove duplicate
wordset = set(); 
for line in f:
    line = line.rstrip()
    words = line.split(" ")
    for word in words:
        if not word.isspace():
            wordset.add(string.lower(word))

# output in reverse order
wordlist = list(wordset)
wordlist.sort(reverse=True)
message = ",".join(wordlist)
sys.stdout.write(message)




        