#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install seaborn


# In[10]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv(r'C:\Users\dicug\Downloads\final_dataset_def.csv')
    

# looking at hypotesis we drop all the columns that aren't needed
# column needed: index, country (we keep this as geographical feature), awards(but we keep only the number -> num_awards), price_range (more accurate than price_level), cuisines, features, veget/vegan/gluten, open_hours_per_week
df=df.drop(columns=['restaurant_name', 'region', 'province', 'city', 'latitude', 'longitude', 'popularity_detailed', 'popularity_generic', 'claimed', 'awards', 'top_tags', 'price_level', 'meals', 'special_diets', 'original_open_hours', 'open_days_per_week', 'working_shifts_per_week'])

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


# In[ ]:




