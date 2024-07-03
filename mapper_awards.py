
import sys
count = 0

for line in sys.stdin:
    line = line.strip()
    splits = line.split(',')
    if (len(splits)>7) and (splits[0].isnumeric()):
        Awards = splits[5]
        id = int(splits[0])
        if Awards == '""':
            print(id, '\t', 0)
        else:
            awards = Awards.split(';')
            k = len(awards)
            for i in range(k):
                print(id, '\t', 1)
    else:
        continue

