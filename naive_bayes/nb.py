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

    # only two parameters
    if len(sys.argv) != 3:
        print(Usage)
        sys.exit()

    # open training data
    try:
        training = open(sys.argv[1])
    except IOError:
        print "cannot open training data"
        sys.exit()

    # open test data
    try:
        dev = open(sys.argv[2])
    except IOError:
        print "cannot open test data"
        sys.exit()

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