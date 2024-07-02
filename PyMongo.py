#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pymongo import MongoClient

# Connessione al server MongoDB (assicurati che il server MongoDB sia in esecuzione)
client = MongoClient('localhost', 27017)

# Seleziona il database
db = client['DB_Proj_DSBDA']

# Seleziona la collezione
collection = db['ProjectDSBDA']

# Esegui una query per leggere i documenti dalla collezione
cursor = collection.find({}).limit(850000)

# Converti i documenti in un DataFrame pandas
df = pd.DataFrame(list(cursor))

# Chiudi la connessione al client MongoDB
client.close()



# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
    
df.replace('', np.nan, inplace=True) # to avoid empty spaces


# looking at hypotesis we drop all the columns that aren't needed
# column needed: index, country (we keep this as geographical feature), awards(but we keep only the number -> num_awards), price_range (more accurate than price_level), cuisines, features, veget/vegan/gluten, open_hours_per_week
df=df.drop(columns=[ '_id', 'restaurant_name', 'region', 'province', 'city', 'latitude', 'longitude', 'popularity_detailed', 'popularity_generic', 'claimed', 'awards', 'top_tags', 'price_level', 'meals', 'special_diets', 'original_open_hours', 'open_days_per_week', 'working_shifts_per_week'])

# keep only avg_rating as column for rating (?)
df=df.drop(columns=['total_reviews_count', 'excellent', 'very_good', 'average', 'poor', 'terrible', 'food', 'service', 'value', 'atmosphere'])

print(df.columns.tolist())
print(len(df.columns.tolist()))
     

# same reasoning of awards with features and cuisines
df['num_features'] = df['features'].apply(lambda x: len(x.split(',')) if isinstance(x, str) and x else 0)
df['num_cuisines'] = df['cuisines'].apply(lambda x: len(x.split(',')) if isinstance(x, str) and x else 0)
df=df.drop(columns=['features', 'cuisines'])

print(df.columns.tolist())
print(len(df.columns.tolist()))
     


# transform price_range in the mean of the range
df['avg_price'] = df['price_range'].apply(lambda x:
    (int(x.split('-')[0].replace('€', '').replace('CHF', '').replace('\xa0', '').replace(',', '')) +
     int(x.split('-')[1].replace('€', '').replace('CHF', '').replace('\xa0', '').replace(',', ''))) / 2
    if isinstance(x, str) and '-' in x else np.nan)

df=df.drop(columns=['price_range'])

print(df.columns.tolist())
print(len(df.columns.tolist()))
   

# correlation matrix

df = pd.get_dummies(df, columns=['country'], drop_first=True)           #one-hot vector

# replace Y/N with True/False
df['vegetarian_friendly'] = df['vegetarian_friendly'].replace({'Y': True, 'N': False})
df['vegan_options'] = df['vegan_options'].replace({'Y': True, 'N': False})
df['gluten_free'] = df['gluten_free'].replace({'Y': True, 'N': False})




# plot matrix


# Converti tutte le colonne in numerico (le stringhe non convertibili diventano NaN)
#df = df.apply(pd.to_numeric, errors='coerce')

# Visualizza i tipi di dati aggiornati
print(df.dtypes)
correlation_matrix = df.corr()
correlation_matrix.style.background_gradient(cmap='coolwarm')



plt.figure(figsize=(20, 20))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()
     


def find_max_value(matrix):
    max_value = None
    max_idx = None
    n = matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if pd.notna(matrix.iloc[i, j]):
                if max_value is None or matrix.iloc[i, j] > max_value:
                    max_value = matrix.iloc[i, j]
                    max_idx = (matrix.index[i], matrix.columns[j])
    return max_value, max_idx

def find_min_value(matrix):
    min_value = None
    min_idx = None
    n = matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if pd.notna(matrix.iloc[i, j]):
                if min_value is None or matrix.iloc[i, j] < min_value:
                    min_value = matrix.iloc[i, j]
                    min_idx = (matrix.index[i], matrix.columns[j])
    return min_value, min_idx

max_value, max_idx = find_max_value(correlation_matrix)
print(f"Max: {max_value} at {max_idx}")

min_value, min_idx = find_min_value(correlation_matrix)
print(f"Min: {min_value} at {min_idx}")


# In[4]:


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

print(df.columns.tolist())
x = df[['vegetarian_friendly', 'vegan_options', 'gluten_free', 'open_hours_per_week',  'population,N,19,11', 'num_awards', 'num_features', 'num_cuisines', 'avg_price', 
'country_England',
'country_France' ,               
'country_Germany' ,               
'country_Italy' ,                
'country_Northern Ireland' ,      
'country_Scotland'  ,            
'country_Spain'   ,               
'country_The Netherlands'  ,      
'country_Wales']]
y = df['avg_rating']


imputer = SimpleImputer(strategy='mean')

x = imputer.fit_transform(x)
y = y.fillna(y.mean())


bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
labels = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
y_binned = pd.cut(y, bins=bins, labels=labels, include_lowest=True).astype(int)

print(y_binned)
x_train, x_test, y_train, y_test = train_test_split(x, y_binned, shuffle = True, train_size = 0.9, random_state=11)

scaler = StandardScaler()
scaler.fit(x_train)
x_train_normalized = scaler.transform(x_train)
x_test_normalized = scaler.transform(x_test)




# In[5]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import mean_squared_error, r2_score

clf = RandomForestClassifier(n_estimators=50)
clf.fit(x_train_normalized, y_train)

y_train_pred = clf.predict(x_train_normalized)
y_test_pred = clf.predict(x_test_normalized)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

confusion_matrix = confusion_matrix(y_test, y_test_pred)

print(f'Training Accuracy: {train_accuracy}')
print(f'Test Accuracy: {test_accuracy}')
print(confusion_matrix)

mse = mean_squared_error(y_test, y_test_pred )
r2_test = r2_score(y_test,  y_test_pred )
r2_train = r2_score(y_train,  y_train_pred )
print(mse, r2_test, r2_train)



# In[6]

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error, r2_score

k = 1

weights = 'uniform'   # Come calcolo la distanza, in questo caso distanza euclidea standard

knn_model = KNeighborsClassifier(n_neighbors=k, weights= weights)
knn_model.fit(x_train_normalized, y_train)
knn_model_predictions = knn_model.predict(x_test_normalized)
knn_model_predictions2 = knn_model.predict(x_train_normalized)
test_accuracy = accuracy_score(knn_model_predictions, y_test)
train_accuracy = accuracy_score(knn_model_predictions2, y_train)
print('accuracy:' , test_accuracy)
print('train_accuracy:', train_accuracy)
conf_matrix = confusion_matrix(y_test, knn_model_predictions)
print('Confusion Matrix:')
print(conf_matrix)
mse = mean_squared_error(y_test, knn_model_predictions )
r2_test = r2_score(y_test, knn_model_predictions)
r2_train = r2_score(y_train, knn_model_predictions2)
print(mse, r2_test, r2_train)


# In[7]

from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import mean_squared_error, r2_score

svc = SVC(kernel = 'rbf', C = 1E10)

svc.fit(x_train, y_train)
y_train_pred = svc.predict(x_train_normalized)
y_test_pred = svc.predict(x_test_normalized)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

confusion_matrix = confusion_matrix(y_test, y_test_pred)

# Stampare l'accuratezza
print(f'Training Accuracy: {train_accuracy}')
print(f'Test Accuracy: {test_accuracy}')
print(confusion_matrix)

