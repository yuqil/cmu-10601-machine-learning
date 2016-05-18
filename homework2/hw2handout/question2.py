#!/usr/bin/python

# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for counting the word

import string
import sys

Usage = "Usage: python question2.py 'path/to/input/'"

# two parameters
if (len(sys.argv) != 2):
    print(Usage)
    
# open input
try:
    f = open(sys.argv[1])
except IOError:
    print "cannot open file"
    sys.exit()

# word count
wordcount = dict();
for line in f:
    line = line.rstrip()
    words = line.split(" ")
    for word in words:
        word = string.lower(word);
        if wordcount.has_key(word):
            wordcount[word] = wordcount[word] + 1
        else :
            wordcount[word] = 1;

# output in reverse order
wordlist = wordcount.keys()
wordlist.sort(reverse=True)
pairs = []
for word in wordlist:
    pairs.append(word + ":" + str(wordcount[word]))
message = ",".join(pairs)
sys.stdout.write(message)
