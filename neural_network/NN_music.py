#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for NN

import sys
import math
import random
import numpy
import time as Time
Usage = "Usage: python NN_music.py testFileName devFile"

step = 0.1
init_weight = 0.5
hidden_size =7

def main():
    global step
    global init_weight
    global hidden_size

    # only two parameters
    if len(sys.argv) != 3:
        print(Usage)
        sys.exit();

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
        print "cannot open develop data"
        sys.exit()

    # get attributes
    line = training.readline().rstrip()
    attributes = line.split(",")
    attributes_size = len(attributes) - 1
    training_data = []
    training_output = []
    max_value = [1999, 6.81]

    # get training data and attribute values
    for line in training:
        line = line.rstrip()
        attributes = line.split(",")
        values = []
        for i in range(0, len(attributes) - 1):
            if attributes[i] == 'yes':
                values.append(1.0)
            elif attributes[i] == 'no':
                values.append(0.0)
            elif i == 0:
                values.append((float(attributes[i]) - 1900) / 100.0)
            elif i == 1:
                values.append(float(attributes[i]) / max_value[i])
        training_data.append(values)
        if attributes[-1] == 'yes':
            training_output.append(1.0)
        elif attributes[-1] == 'no':
            training_output.append(0.0)

    # NN set up
    root = Node(hidden_size, init_weight)
    hidden_layer = []
    for i in range(0, hidden_size):
        hidden_layer.append(Node(attributes_size, init_weight))

    # train weight
    elapse = 0
    start = Time.time()
    while elapse < 100:
        mse = train_weight(root, hidden_layer, training_data, training_output)
        print mse
        end = Time.time()
        elapse = end - start

    training.close()
    print "TRAINING COMPLETED! NOW PREDICTING."

    dev.readline()
    # get training data and attribute values
    for line in dev:
        line = line.rstrip()
        attributes = line.split(",")
        values = []
        for i in range(0, len(attributes)):
            if attributes[i] == 'yes':
                values.append(1.0)
            elif attributes[i] == 'no':
                values.append(0.0)
            elif i == 0:
                values.append((float(attributes[i]) - 1900) / 100.0)
            elif i == 1:
                values.append(float(attributes[i]) / max_value[i])
        middle = []
        for h in range(0, len(hidden_layer)):
            middle.append(hidden_layer[h].compute(values))
        o_k = root.compute(middle)
        #print o_k
        if (o_k > 0.5): print "yes"
        else: print "no"


def train_weight(root, hidden_layer, training_data, training_output):
    global step
    mse = 0.0
    for k in range(0, len(training_data)):
        # get output
        middle = []
        for h in range(0, len(hidden_layer)):
            middle.append(hidden_layer[h].compute(training_data[k]))
        o_k = root.compute(middle)
        mse += (training_output[k] - o_k) ** 2

        # compute delta
        delta_k = o_k * (1.0 - o_k) * (training_output[k] - o_k)
        delta_h = []
        data_len = len(training_data[0])
        for h in range(0, len(hidden_layer)):
            delta_h.append(middle[h] * (1 - middle[h]) * root.weight[h] * delta_k)
            root.weight[h] += (step * middle[h] * delta_k)
            for i in range(0, data_len):
                hidden_layer[h].weight[i] += (step * delta_h[h] * training_data[k][i])

    return mse


class Node(object):
    def __init__(self, size, initial_value):
        self.weight = []
        self.size = size
        for i in range(0, size):
            self.weight.append(random.uniform(-1 * initial_value, initial_value))

    def compute(self, data):
        result = 0
        for i in range(0, len(data)):
            result += (data[i] * self.weight[i])
        return signoid(result)


def signoid(y):
    result = 1.0 / (1 + math.exp(-1 * y))
    return result


def dif_signoid(y):
    tmp = signoid(y)
    return tmp * (1 - tmp)


if __name__ == '__main__':
    main()