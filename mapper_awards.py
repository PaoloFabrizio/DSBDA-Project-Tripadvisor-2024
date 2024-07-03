
import sys
count = 0

for line in sys.stdin:
    line = line.strip()
    splits = line.split(',')
    
    id = splits[0]
    restaurant_name = splits[1]
    country = splits[2]
    city = splits[3]
    Awards = splits[4]
    price_range = splits[5]
    cuisines = splits[6]
    features = splits[7]
    vegetarian = splits[8]
    vegan = splits[9]
    gluten_free = splits[10]
    open_hours_per_week = splits[11]
    avg_rating = splits[12]
    
    if (len(splits)>7) and (splits[0].isnumeric()):
        id = int(id)
        if Awards == '""':
            
            print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', Awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', 0)
            
        else:
            awards = Awards.split(';')
            k = len(awards)
            for i in range(k):
                
                print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', Awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', 1)
                
    elif splits[0].isnumeric()==False:
        
        print(id, '\t', restaurant_name, '\t', country, '\t', city, '\t', Awards, '\t', price_range, '\t', cuisines, '\t', features, '\t', vegetarian, '\t', vegan, '\t', gluten_free, '\t', open_hours_per_week, '\t', avg_rating, '\t', 'n_awards')
    
    else:
        continue
