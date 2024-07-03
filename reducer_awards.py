import sys

current_id = 0
count = 0

for line in sys.stdin:
    line = line.strip()
    splits = line.split('\t')
    
    id = splits[0]
    restaurant_name = splits[1]
    country = splits[2]
    city = splits[3]
    awards = splits[4]
    price_range = splits[5]
    cuisines = splits[6]
    features = splits[7]
    vegetarian = splits[8]
    vegan = splits[9]
    gluten_free = splits[10]
    open_hours_per_week = splits[11]
    avg_rating = splits[12]
    n_awards = splits[13]

    if splits[0].isnumeric()==True:

        id = int(id)
        n_awards = int(n_awards)
        
        if ((id != current_id) and (n_awards==0) and (count==0)):   # new restaurant with zero awards
            current_id = id
            count = 0
            print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', count)
        elif ((id != current_id) and (n_awards!=0) and (count==0)):   #new restaurant with awards
            count+= n_awards
            current_id = id
        elif ((id == current_id) and (n_awards!=0)): #restaurant with awards already seen
            count+= n_awards
        elif ((id != current_id) and (n_awards==0) and (count>0)):  # new restaurant with zero awards
            print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', count)
            count = 0
            current_id = id
            print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', count)
        elif ((id != current_id) and (n_awards!=0) and (count>0)):
            print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', count)
            count=0
            count += n_awards
            current_id = id
        else:
            continue

    else:
        print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', 'n_awards')

        