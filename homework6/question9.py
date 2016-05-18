import sys
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


    # E(temp), E(cnt)
    items = 0
    cnt = 0
    cnttemp = 0
    temp = attributes_name.index("temp")
    count = attributes_name.index("cnt")
    for i in range(0, size):
        items += float(attributes[temp][i])
        cnt += int(attributes[count][i])
        cnttemp += (float(attributes[temp][i]) * int(attributes[count][i]))
    e_temp = float(items) / size
    e_cnt = float(cnt) / size
    e_cnttemp = float(cnttemp) / size

    # VAR(temp)
    items = 0
    temp = attributes_name.index("temp")
    for i in range(0, size):
        items += ((float(attributes[temp][i]) - e_temp) * (float(attributes[temp][i]) - e_temp))
    var_temp = float(items) / size

    cov_tempcnt = e_cnttemp - e_cnt * e_temp
    b = cov_tempcnt / var_temp
    a = e_cnt - b * e_temp

    mse = 0
    for i in range(0, size):
        mse += (a + b * float(attributes[temp][i]) - int(attributes[count][i])) * (a + b * float(attributes[temp][i]) - int(attributes[count][i]))
    mse = mse / size

    print a
    print b
    print mse
    print a + b * 0.55

if __name__ == '__main__':
    main()
