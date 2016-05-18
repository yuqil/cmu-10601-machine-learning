#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for HMM

import sys
import math
import operator
import copy
from math import *

Usage = "Usage: python viterbi.py <dev> <hmm-trans> <hmm-emit> <hmm-prior> "


def main():
    pi = []
    A = {}
    B = {}
    states = []

    # only four parameters
    if len(sys.argv) != 5:
        print(Usage)
        sys.exit()

    # open training data
    try:
        dev = open(sys.argv[1])
    except IOError:
        print "cannot open training data"
        sys.exit()

    # open test data
    try:
        trans = open(sys.argv[2])
    except IOError:
        print "cannot open trans data"
        sys.exit()

    # open test data
    try:
        emit = open(sys.argv[3])
    except IOError:
        print "cannot open emit data"
        sys.exit()

    # open test data
    try:
        prior = open(sys.argv[4])
    except IOError:
        print "cannot open prior data"
        sys.exit()

    # get prior probability
    for line in prior:
        line = line.rstrip()
        tokens = line.split(" ")
        item = (tokens[0], tokens[1])
        pi.append(item)
        states.append(tokens[0])
    prior.close()

    # get trans probability
    for line in trans:
        line = line.rstrip()
        tokens = line.split(" ")
        i = tokens[0]
        A[i] = {}
        for k in range(1, len(tokens)):
            items = tokens[k].split(":")
            j = items[0]
            A[i][j] = float(items[1])
    trans.close()

    # get emit probability
    for line in emit:
        line = line.rstrip()
        tokens = line.split(" ")
        i = tokens[0]
        B[i] = {}
        for j in range(1, len(tokens)):
            items = tokens[j].split(":")
            k = items[0]
            B[i][k] = float(items[1])
    emit.close()

    # Vertibi Algorithms
    state_num = len(pi)
    for line in dev:
        line = line.rstrip()
        words = line.split(" ")
        T = len(words)
        alpha = [[0 for x in range(state_num)] for x in range(1 + T)]
        Q = [[[] for x in range(state_num)] for x in range(1 + T)]

        for i in range(0, state_num):
            pi_i = float(pi[i][1])
            bi_ok = float(B[pi[i][0]][words[0]])
            alpha[1][i] = math.log(pi_i) + math.log(bi_ok)
            Q[1][i] = [i]

        for t in range(1, len(words)):
            for i in range(0, state_num):
                k = 0
                tmp = alpha[t][0] + math.log(A[states[0]][states[i]]) + math.log(B[states[i]][words[t]])
                for j in range(1, state_num):
                    if tmp < (alpha[t][j] + math.log(A[states[j]][states[i]]) + math.log(B[states[i]][words[t]])):
                        tmp = (alpha[t][j] + math.log(A[states[j]][states[i]]) + math.log(B[states[i]][words[t]]))
                        k = j
                alpha[t + 1][i] = tmp
                past = copy.deepcopy(Q[t][k])
                past.append(i)
                Q[t + 1][i] = past

        k = 0
        tmp = alpha[T][0]
        for i in range(state_num):
            if alpha[T][i] > tmp:
                tmp = alpha[T][i]
                k = i
        msg = ""
        for i in range(len(Q[T][k])):
            msg += (words[i] + "_" + states[Q[T][k][i]])
            if i != len(Q[T][k]) - 1:
                msg += " "
        print msg


# computes log sum of two exponentiated log numbers efficiently
def log_sum(left, right):
    if right < left:
        return left + log1p(exp(right - left))
    elif left < right:
        return right + log1p(exp(left - right));
    else:
        return left + log1p(1)


if __name__ == '__main__':
    main()
