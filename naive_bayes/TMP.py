#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for naive bayes

import sys
import math
import operator
Usage = "Usage: python nb.py split.train split.test"


def main():
    vocabulary = set()
    text_lib = {}
    text_con = {}

        # open training data
    try:
        training = open("/Users/yuqil/Desktop/second semester/11642/QryEval/queries copy.txt")
    except IOError:
        print "cannot open training data"
        sys.exit()

    for line in training:
        line = line.rstrip();
        tokens = line.split(":")
        query = tokens[1]
        print "print \"" + tokens[0] + ":\" ;"
        print "print formulate_query( \"" + query + "\", \"sd\" , $w1, $w2, $w3) . \"\\n\";"


if __name__ == "__main__":
    main()
