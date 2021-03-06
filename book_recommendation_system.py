# -*- coding: utf-8 -*-
"""Book_Recommendation_System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P8Gl7UgZtUAykD470UqwURVnFfT6TZl5

# Importing Modules
"""

import numpy as np
import pandas as pd

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline

# Load dataframe
df = pd.read_csv('/content/drive/MyDrive/DATA/books_10K/books.csv',error_bad_lines= False)
df.head()

df.columns

df.isnull().sum()

df.info()

df.describe()

"""# Visualization"""

top_fifteen = df[df['ratings_count'] > 1000000]
top_fifteen.sort_values(by='average_rating', ascending=False)
top_fifteen.head(15)

plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(10, 10))

data = top_fifteen.sort_values(by='average_rating', ascending=False).head(15)
gr = sns.barplot(x="average_rating", y="title", data=data, palette="CMRmap_r")

for i in gr.patches:
    gr.text(i.get_width() + .05, i.get_y() + 0.5, str(i.get_width()), fontsize = 10, color = 'k')
plt.show()

top_15_authors = df.groupby('authors')['title'].count().reset_index().sort_values('title', ascending=False).head(15).set_index('authors')
top_15_authors.head(15)

plt.figure(figsize=(15,10))
ax = sns.barplot(top_15_authors['title'], top_15_authors.index, palette='CMRmap_r')

ax.set_title("Top 10 authors with most books")
ax.set_xlabel("Total number of books")
totals = []
for i in ax.patches:
    totals.append(i.get_width())
total = sum(totals)
for i in ax.patches:
    ax.text(i.get_width()+.2, i.get_y()+.2,str(round(i.get_width())), fontsize=15,color='black')
plt.show()

ax = sns.relplot(data=df,
                 x="ratings_count",
                 y="average_rating",
                 color = '#95a3c3',
                 sizes=(400, 600), 
                 height=7, 
                 marker='o')

plt.figure(figsize=(15, 7))
ax = sns.countplot(x=df.language_code, data=df)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x()-0.05, p.get_height()+100))

top_15_publisher = df.groupby('publisher')['title'].count().reset_index().sort_values('title', ascending=False).head(15).set_index('publisher')
top_15_publisher.head(15)

plt.figure(figsize=(15,10))
ax = sns.barplot(top_15_publisher['title'], top_15_publisher.index, palette='CMRmap_r')

ax.set_title("Top 15 publisher with most books")
ax.set_xlabel("Total number of books")
totals = []
for i in ax.patches:
    totals.append(i.get_width())
total = sum(totals)
for i in ax.patches:
    ax.text(i.get_width()+.2, i.get_y()+.2,str(round(i.get_width())), fontsize=15,color='black')
plt.show()

df.average_rating = df.average_rating.astype(float)
fig, ax = plt.subplots(figsize=[15,10])
sns.distplot(df['average_rating'],ax=ax)
ax.set_title('Average rating distribution for all books',fontsize=20)
ax.set_xlabel('Average rating',fontsize=13)



"""# Feature Engineering"""

df.columns

threshold = 0.7
df = df[df.columns[df.isnull().mean() < threshold]]
df = df.loc[df.isnull().mean(axis=1) < threshold]

df.head()

corrmat = df.corr()   
f, ax = plt.subplots(figsize =(9, 8)) 
sns.heatmap(corrmat, ax = ax, cmap ="YlGnBu", linewidths = 0.1)

df2 =df.copy()

df2.loc[ (df2['average_rating'] >= 0) & (df2['average_rating'] <= 1), 'rating_between'] = "between 0 and 1"
df2.loc[ (df2['average_rating'] > 1) & (df2['average_rating'] <= 2), 'rating_between'] = "between 1 and 2"
df2.loc[ (df2['average_rating'] > 2) & (df2['average_rating'] <= 3), 'rating_between'] = "between 2 and 3"
df2.loc[ (df2['average_rating'] > 3) & (df2['average_rating'] <= 4), 'rating_between'] = "between 3 and 4"
df2.loc[ (df2['average_rating'] > 4) & (df2['average_rating'] <= 5), 'rating_between'] = "between 4 and 5"

df2.head()

rating_df = pd.get_dummies(df2['rating_between'])
rating_df.head()

l_code_df = pd.get_dummies(df2['language_code'])
l_code_df.head()

features = pd.concat([l_code_df, rating_df, df2['average_rating'], df2['ratings_count']], axis=1)
features.head()

"""# Model Building"""

from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

min_max_scaler = MinMaxScaler()
features = min_max_scaler.fit_transform(features)

model = neighbors.NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
model.fit(features)
dist, idlist = model.kneighbors(features)

idlist

def book_recommendation_engine(book_name):
    book_list_name = []
    book_id = df2[df2['publisher'].astype(str).str.contains(book_name)].index
    print(book_id)
    book_id = book_id[0]
    for newid in idlist[book_id]:
        book_list_name.append(df2.loc[newid].title)
    return book_list_name

book_list_name = book_recommendation_engine('Scholastic')
book_list_name

import pickle

df2.tail()

df2[df2.isbn == '0609804618']

