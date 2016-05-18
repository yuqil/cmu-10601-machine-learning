#!/usr/bin/python

# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for removing stop words

import string
import sys

Usage = "Usage: python question3.py 'path/to/input/' 'path/to/stopwords/file'"

# three parameters
if (len(sys.argv) != 3):
    print(Usage)

# open stop word file
try:
    f = open(sys.argv[2])
except IOError:
    print "cannot open file" + sys.argv[2]
    sys.exit()

# get stop words    
stopword = set()
for line in f:
    line = line.rstrip()
    stopword.add(string.lower(line))

# open input file
wordcount = dict();
try:
    f = open(sys.argv[1])
except IOError:
  print "cannot open file" + sys.argv[1]
  sys.exit()
  
# word count except for stop word
for line in f:
    line = line.rstrip()
    words = line.split(" ")
    for word in words:
        word = string.lower(word);
        if word in stopword: 
            continue
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