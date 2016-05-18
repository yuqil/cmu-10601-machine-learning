#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for list-then-eliminate algorithm

import sys
import copy
Usage = "Usage: python partB.py testFileName"


def main():
    # only one parameters
    if len(sys.argv) != 2:
        print(Usage)
        sys.exit();

    # print size of x
    x = 2 ** 4
    print str(x)

    # print size of concept space
    c = 2 ** x
    print str(c)

    # build concept space
    conceptspc = build_concept_space(16)
    versionspc = list_eliminate(conceptspc)
    print str(len(versionspc))

    # test data
    test_data(versionspc)


def test_data(conceptspc):
    # open test data
    try:
        f = open(sys.argv[1])
    except IOError:
        print "cannot open file" + sys.argv[1]
        sys.exit()
    for line in f:
        line.rstrip()
        attributes = line.split("\t")
        index = get_index(attributes)
        high = 0
        low = 0
        for concept in conceptspc:
            if concept[index] == 1:
                high += 1
            else:
                low += 1
        print str(high) + " " + str(low)
    f.close()


# list then eliminate algorithm
def list_eliminate(conceptspc):
    # open training data
    try:
        f = open("4Cat-Train.labeled")
    except IOError:
        print "cannot open file 9Cat-Train.labeled"
        sys.exit()

    for line in f:
        line.rstrip()
        attributes = line.split("\t")
        risk = 0
        if attributes[4].split(" ")[1] == 'high':
            risk = 1
        index = get_index(attributes)
        conceptspc = [concept for concept in conceptspc if concept[index] == risk]
    f.close()
    return conceptspc


# get index of the data
def get_index(attributes):
    case = 0;
    for i in range(0, 4):
        attribute = attributes[i].split(" ")
        if attribute[1] == 'Male':
            case += 8
        if attribute[1] == 'Young':
            case += 4
        if attribute[1] == 'Yes' and attribute[0] == 'Student?':
            case += 2
        if attribute[1] == 'Yes' and attribute[0] == 'PreviouslyDeclined?':
            case += 1
    return case


# build concept space
def build_concept_space(num):
    conceptspc = [[]]
    for i in range(0, num):
        tmp1 = copy.deepcopy(conceptspc)
        for concept in tmp1:
            concept.insert(0, 1)
        tmp2 = copy.deepcopy(conceptspc)
        for concept in tmp2:
            concept.insert(0, 0)
        conceptspc = tmp1 + tmp2
    return conceptspc


if __name__ == '__main__':
    main()
