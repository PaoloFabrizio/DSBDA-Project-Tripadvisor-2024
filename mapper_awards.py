import sys

for line in sys.stdin:
    line = line.strip()
    splits = line.split(',')
    if len(splits)>7:
        Awards = splits[8]
        Restaurant = splits[1]
        id = splits[0]
        if Awards == '""':
            print(Restaurant, '\t' ,id, '\t', 0)
        else:
            awards = Awards.split(';')
            k = len(awards)
            for i in range(k):
                print(Restaurant, '\t' ,id, '\t', 1)
    else:
        continue