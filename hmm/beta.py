#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for HMM

import sys
import math
import operator
from math import *

Usage = "Usage: python beta.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>"


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

    # Backward Algorithms
    state_num = len(pi)
    for line in dev:
        line = line.rstrip()
        words = line.split(" ")
        T = len(words)
        beta = [[0 for x in range(state_num)] for x in range(1 + T)]
        for i in range(0, state_num):
            beta[T][i] = log(1)

        for t in range(T-1, 0, -1):
            for i in range(state_num):
                tmp = beta[t+1][0] + math.log(A[states[i]][states[0]]) + math.log(B[states[0]][words[t]])
                for j in range(1, state_num):
                    tmp = log_sum(tmp, beta[t+1][j] + math.log(A[states[i]][states[j]]) + math.log(B[states[j]][words[t]]))
                beta[t][i] = tmp
        p_o_lumda = beta[1][0] + math.log(float(pi[0][1])) + math.log(B[states[0]][words[0]])

        for i in range(1, state_num):
            p_o_lumda = log_sum(p_o_lumda, beta[1][i] + math.log(float(pi[i][1])) + math.log(B[states[i]][words[0]]))
        print p_o_lumda


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
