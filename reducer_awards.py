import sys

current_id = 0
current_restaurant = None
count = 0

for line in sys.stdin:
    line = line.strip()
    splits = line.split('\t')
    #print(splits)
    if ((splits[1] != current_id) and (int(splits[2])==0) and (count==0)):   # new restaurant with zero awards
        current_id = splits[1]
        current_restaurant = splits[0]
        count = 0
        print(current_id, '\t', current_restaurant, '\t', count)
        
    elif ((splits[1] != current_id) and (int(splits[2])!=0) and (count==0)):   #new restaurant with awards
        count+=int(splits[2])
        current_id = splits[1]
        current_restaurant = splits[0]
    elif ((splits[1] == current_id) and (int(splits[2])!=0)): #restaurant with awards already seen
        count+=int(splits[2])
    elif ((splits[1] != current_id) and (int(splits[2])==0) and (count>0)):  # new restaurant with zero awards
        print(current_id, '\t', current_restaurant, '\t', count)
        count = 0
        current_id = splits[1]
        current_restaurant = splits[0]
        print(current_id, '\t', current_restaurant, '\t', count)
    elif ((splits[1] != current_id) and (int(splits[2])!=0) and (count>0)):
        print(current_id, '\t', current_restaurant, '\t', count)
        count=0
        count += int(splits[2])
        current_id = splits[1]
        current_restaurant = splits[0]
    else:
        continue