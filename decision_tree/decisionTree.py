#!/usr/bin/python
# Author: YUQI LIU(Andrew ID: yuqil)
# This is a program for training decision tree

import sys
import copy
import math

Usage = "Usage: python decisionTree.py trainingData testFileName"
# all attributes
attributes = []
# all attributes's values
attributes_values = {}
negative_label = ""
positive_label = ""


def main():
    global attributes
    global attributes_values
    global negative_label
    global positive_label

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
        print "cannot open test data"
        sys.exit()

    # get attributes
    line = training.readline().rstrip()
    attributes = line.split(",")
    attributes = [x.strip(' ') for x in attributes]
    for attribute in attributes:
        attribute = attribute.strip()
        attributes_values[attribute] = []
    training_data = []

    # get training data and attribute values
    for line in training:
        line = line.rstrip()
        values = line.split(",")
        values = [x.strip(' ') for x in values]
        training_data.append(values)
        for i in range(0, len(attributes)):
            if values[i] not in attributes_values[attributes[i]]:
                values[i] = values[i].strip()
                attributes_values[attributes[i]].append(values[i])

    # get output label
    for label in attributes_values[attributes[-1]]:
        if 'n' in label:
            negative_label = label
        else:
            positive_label = label
    attributes.remove(attributes[-1])

    # train tree and print
    root = Node('root', attributes, training_data)
    root = train_tree(root, 1)
    print "[" + str(len(root.positive)) + "+/" + str(len(root.negative)) + "-]"
    print_tree(root, "")

    # evaluate tree
    training.seek(0)
    training.readline()
    dev.readline()
    print "error(train): " + str(evaluate_tree(root, training))
    print "error(test): " + str(evaluate_tree(root, dev))
    dev.close()
    training.close()


# train tree in recursive way, stop when I < 0.1 or height > 2
def train_tree(crt, height):
    crt.calculate_mutual_information()
    if len(crt.mutual_entropy) == 0 or max(crt.mutual_entropy) < 0.1 or height > 2:
        return crt

    max_index = crt.mutual_entropy.index(max(crt.mutual_entropy))
    variable = copy.deepcopy(crt.variables[max_index])
    variables = copy.deepcopy(crt.variables)
    variables.remove(variable)
    crt.variable = variable

    left = Node('root', variables, crt.split_data(max_index, 0))
    left.set_key(attributes_values[variable][0])
    right = Node('root', variables, crt.split_data(max_index, 1))
    right.set_key(attributes_values[variable][1])

    left = train_tree(left, height + 1)
    right = train_tree(right, height + 1)

    crt.children.append(left)
    crt.children.append(right)
    return crt


# Print tree using DFS
def print_tree(root, prefix):
    if len(root.children) == 0:
        return
    for child in root.children:
        print prefix + root.variable + " = " + child.key + ": [" + str(len(child.positive)) + "+/" + str(len(child.negative)) + "-]"
        if child.variable != 'root':
            print_tree(child, "| " + prefix)


# evaluate tree from test data, return error value
def evaluate_tree(root, test):
    global attributes
    global negative_label
    global positive_label

    size = 0
    error = 0
    for line in test:
        size += 1
        line = line.rstrip()
        values = line.split(",")
        values = [x.strip(' ') for x in values]
        crt = root
        while len(crt.children) != 0:
            index = attributes.index(crt.variable)
            value = values[index]
            for child in crt.children:
                if child.key == value:
                    crt = child
                    break
        label = values[-1]
        if len(crt.positive) > len(crt.negative):
            if label == negative_label:
                error += 1
        else:
            if label == positive_label:
                error += 1
    return float(error) / size


# calculate entropy
def cal_entropy(pos, neg):
    if pos == 0 or neg == 0:
        return 0
    total = pos + neg
    p_pos = float(pos) / total
    p_neg = float(neg) / total
    etp = p_pos * math.log(1.0 / p_pos, 2) + p_neg * math.log(1.0 / p_neg, 2)
    return etp


# treenode class
class Node(object):
    def __init__(self, variable, variables=[], datas=[]):
        global attributes
        global attributes_values
        global negative_label
        self.children = []           # if split, has children
        self.variable = variable     # split on this variable
        self.variables = variables   # all remaining attributes
        self.negative = []           # negative data
        self.positive = []           # positive data
        self.mutual_entropy = []     # mutual entropy of remaining attributes
        self.key = 'default'         # key is parent's split value
        for data in datas:
            if data[-1] == negative_label:
                self.negative.append(data)
            else:
                self.positive.append(data)
        self.entropy = cal_entropy(len(self.positive), len(self.negative))

    # calculate mutual information for remaining attributes, store in mutual_entropy
    def calculate_mutual_information(self):
        global attributes_values
        global attributes

        for variable in self.variables:
            index = attributes.index(variable)
            val1_pos = 0
            val2_pos = 0
            val1_neg = 0
            val2_neg = 0
            for data in self.positive:
                if data[index] == attributes_values[variable][0]:
                    val1_pos += 1
                else:
                    val2_pos += 1

            for data in self.negative:
                if data[index] == attributes_values[variable][0]:
                    val1_neg += 1
                else:
                    val2_neg += 1

            total_size = len(self.positive) + len(self.negative)
            p_val1 = float(val1_pos + val1_neg) / total_size
            p_val2 = float(val2_pos + val2_neg) / total_size
            mutual_information = self.entropy - p_val1 * cal_entropy(val1_pos, val1_neg) - p_val2 * cal_entropy(
                    val2_pos, val2_neg)
            self.mutual_entropy.append(mutual_information)

    # split data on variable[max_index], the value is state
    def split_data(self, max_index, state):
        global attributes_values
        global attributes
        result = []
        variable = self.variables[max_index]
        index = attributes.index(variable)
        for data in self.positive:
            if data[index] == attributes_values[variable][state]:
                result.append(data)
        for data in self.negative:
            if data[index] == attributes_values[variable][state]:
                result.append(data)
        return result

    # set key
    def set_key(self, key):
        self.key = key


if __name__ == '__main__':
    main()
