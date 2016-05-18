import sys
import numpy as np
from numpy.linalg import inv
Usage = "Usage: python question7.py csvfile "


def main():
    # only one parameters
    if len(sys.argv) != 2:
        print(Usage)
        sys.exit();

    # open test data
    try:
        f = open(sys.argv[1])
    except IOError:
        print "cannot open file" + sys.argv[1]
        sys.exit()

    # read data
    first_line = f.readline().rstrip();
    attributes_name = first_line.split(",")
    attributes = [[] for x in range(0, len(attributes_name))]
    for line in f:
        line = line.rstrip()
        values = line.split(",")
        for i in range(0, len(values)):
            attributes[i].append(values[i])
    size = len(attributes[1])

    # Y
    Y = [[] for x in range(0, size)]
    cnt = attributes_name.index("cnt")
    for i in range(0, size):
        Y[i].append(int(attributes[cnt][i]))
    Y2 = np.array(Y)

    # X
    X = [[] for x in range(0, size)]
    temp = attributes_name.index("temp")
    hum = attributes_name.index("hum")
    for i in range(0, size):
        X[i].append(1.0)
        X[i].append(float(attributes[temp][i]))
        X[i].append(float(attributes[hum][i]))

    # B
    X = np.array(X)
    X_T = np.transpose(X)
    B = np.dot(inv(np.dot(X_T, X)), np.dot(X_T, Y))

    # output result
    print B[0][0]
    print B[1][0]
    print B[2][0]

    mse = 0
    temp = attributes_name.index("temp")
    hum = attributes_name.index("hum")
    for i in range(0, size):
        x = []
        x.append(1.0)
        x.append(float(attributes[temp][i]))
        x.append(float(attributes[hum][i]))
        y = np.dot(x, B)
        mse += (int(attributes[cnt][i]) - y[0]) * (int(attributes[cnt][i]) - y[0])
    mse = mse / size
    print mse

    x = np.array([1, 0.55, 0.46])
    y = np.dot(x, B)
    print y[0]


if __name__ == '__main__':
    main()