#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for topwords

import sys
import math
import operator
Usage = "Usage: python topwords.py split.train"


def main():
    vocabulary = set()
    text_lib = {}
    text_con = {}

    # only two parameters
    if len(sys.argv) != 2:
        print(Usage)
        sys.exit()

    # open training data
    try:
        training = open(sys.argv[1])
    except IOError:
        print "cannot open training data"
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

    sorted_lib = sorted(text_lib.items(), key=operator.itemgetter(1), reverse=True)
    sorted_con = sorted(text_con.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0, 20):
        print (sorted_lib[i][0] + " " + "%.04f" % sorted_lib[i][1])
    print
    for i in range(0, 20):
        print (sorted_con[i][0] + " " + "%.04f" % sorted_con[i][1])

if __name__ == '__main__':
    main()