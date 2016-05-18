#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for naive bayes

import sys
import math
import operator
Usage = "Usage: python nbStopWords.py split.train split.test 10"


def main():
    vocabulary1 = {}
    text_lib = {}
    text_con = {}

    # only two parameters
    if len(sys.argv) != 4:
        print(Usage)
        sys.exit()

    N = int(sys.argv[3])

    # open training data
    try:
        training1 = open(sys.argv[1])
    except IOError:
        print "cannot open training data"
        sys.exit()

    # open test data
    try:
        dev = open(sys.argv[2])
    except IOError:
        print "cannot open test data"
        sys.exit()

    for line in training1:
        line = line.rstrip()
        blog = open(line)
        for word in blog:
            word = word.rstrip()
            word = word.lower()
            if vocabulary1.has_key(word):
                vocabulary1[word] += 1
            else:
                vocabulary1[word] = 1
    training1.close()

    # get top N words
    sorted_voc = sorted(vocabulary1.items(), key=operator.itemgetter(1), reverse=True)
    topN = []
    for i in range(0, N):
        topN.append(sorted_voc[i][0])

    # open training data
    try:
        training = open(sys.argv[1])
    except IOError:
        print "cannot open training data"
        sys.exit()
    vocabulary = set()

    # get training data and all vocabulary
    lib_num = 0
    con_num = 0
    examples = 0
    lib_pos = 0
    con_pos = 0
    for line in training:
        examples += 1
        line = line.rstrip()
        blog = open(line)
        if line.startswith("lib"):
            lib_num += 1
        else:
            con_num += 1
        for word in blog:
            word = word.rstrip()
            word = word.lower()
            if word in topN:
                continue
            vocabulary.add(word)
            if line.startswith("lib"):
                lib_pos += 1
                if text_lib.has_key(word):
                    text_lib[word] += 1
                else:
                    text_lib[word] = 1
            else:
                con_pos += 1
                if text_con.has_key(word):
                    text_con[word] += 1
                else:
                    text_con[word] = 1
        blog.close()
    training.close()

    # get possibility distribution
    p_lib = float(lib_num) / examples
    p_con = float(con_num) / examples
    len_voc = len(vocabulary)

    for word in vocabulary:
        if text_lib.has_key(word):
            nk = text_lib[word]
            p_wk_lib = float(nk + 1) / (len_voc + lib_pos)
        else:
            p_wk_lib = float(1) / (len_voc + lib_pos)
        text_lib[word] = p_wk_lib
        if text_con.has_key(word):
            nk = text_con[word]
            p_wk_con = float(nk + 1) / (len_voc + con_pos)
        else:
            p_wk_con = float(1) / (len_voc + con_pos)
        text_con[word] = p_wk_con

    # test on dev data
    total = 0
    wrong = 0
    for line in dev:
        total += 1
        line = line.rstrip()
        blog = open(line)
        lib_blog = math.log(p_lib)
        con_blog = math.log(p_con)
        for word in blog:
            word = word.rstrip()
            word = word.lower()
            if not text_con.has_key(word):
                continue
            lib_blog += math.log(text_lib[word])
            con_blog += math.log(text_con[word])
        if lib_blog > con_blog:
            if line.startswith("lib"):
                wrong += 1
            print("L")
        else:
            if line.startswith("con"):
                wrong += 1
            print("C")
    print ("Accuracy: " + "%.04f" % (float(wrong) / total))
    dev.close()

if __name__ == '__main__':
    main()