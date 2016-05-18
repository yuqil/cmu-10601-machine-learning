import sys
import math
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

    # P (hum > 0.6, weathersit = 2 | month > 3, month < 11)
    items = 0
    total = 0
    hum = attributes_name.index('hum')
    month = attributes_name.index('mnth')
    weathersit = attributes_name.index('weathersit')
    for i in range(0, size):
        if 3 < int(attributes[month][i]) < 11:
            total += 1
            if float(attributes[hum][i]) > 0.6 and int(attributes[weathersit][i]) == 2:
                items += 1
    print str(float(items) / total)

    # E(temp)
    items = 0
    temp = attributes_name.index("temp")
    for i in range(0, size):
        items += float(attributes[temp][i])
    print str(float(items) / size)
    e_temp = float(items) / size

    # E(hum)
    items = 0
    temp = attributes_name.index("hum")
    for i in range(0, size):
        items += float(attributes[temp][i])
    print str(float(items) / size)
    e_hum = float(items) / size

    # E(cnt | temp < 0.3)
    items = 0
    total = 0
    cnt = attributes_name.index("cnt")
    temp = attributes_name.index("temp")
    for i in range(0, size):
        if float(attributes[temp][i]) < 0.3:
            total += 1
            items += int(attributes[cnt][i])
    print str(float(items) / total)

    # Var(cnt | temp > 0.3)
    # E(cnt | temp > 0.3)
    items = 0
    total = 0
    cnt = attributes_name.index("cnt")
    temp = attributes_name.index("temp")
    for i in range(0, size):
        if float(attributes[temp][i]) > 0.3:
            total += 1
            items += int(attributes[cnt][i])

    avg = float(items) / total
    items = 0
    cnt = attributes_name.index("cnt")
    temp = attributes_name.index("temp")
    for i in range(0, size):
        if float(attributes[temp][i]) > 0.3:
            items += math.pow(float(int(attributes[cnt][i])), 2)
    print str(float(items) / total - avg * avg)

    # Cov(temp, atemp)
    # E(atemp)
    items = 0
    atemp = attributes_name.index("atemp")
    for i in range(0, size):
        items += float(attributes[atemp][i])
    e_atemp = float(items) / size
    # E(temp * atemp)
    items = 0
    temp = attributes_name.index("temp")
    atemp = attributes_name.index("atemp")
    for i in range(0, size):
        items += (float(attributes[atemp][i]) * float(attributes[temp][i]))
    e_tempatemp = float(items) / size
    print str(e_tempatemp - e_temp * e_atemp)

    # Cor(temp, hum)
    var_temp = 0
    var_hum = 0
    e_humtemp = 0
    temp = attributes_name.index("temp")
    hum = attributes_name.index("hum")
    for i in range(0, size):
        var_temp += math.pow((float(attributes[temp][i]) - e_temp), 2)
        var_hum += math.pow((float(attributes[hum][i]) - e_hum), 2)
        e_humtemp += (float(attributes[temp][i]) * float(attributes[hum][i]))
    var_hum /= size
    var_temp /= size
    e_humtemp /= size
    print str((e_humtemp - e_hum * e_temp) / math.sqrt(var_hum) / math.sqrt(var_temp))

if __name__ == '__main__':
    main()
