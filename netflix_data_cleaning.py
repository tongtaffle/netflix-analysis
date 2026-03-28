# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 23:12:07 2026

@author: Tongtaffle
"""

import pandas as pd

import ast

import chardet

with open("titles.csv", 'rb') as f:
    result = chardet.detect(f.read(100000))

print(result)

title = pd.read_csv("titles.csv", encoding='latin-1')
credit = pd.read_csv("credits.csv", encoding= 'latin-1')

# Overview data #
title.info()
title.head()

credit.info()
credit.head()

# Handle Missing Values #
print(' +++ Handle Missing Values+++ ')
print("titles.csv")
print(title.isnull().sum())
# Drop important nissing
title = title.dropna(subset='title')
# fill text
title["description"] = title["description"].fillna("No description")
title["age_certification"] = title["age_certification"].fillna("Unknown")
title['imdb_id'] = title['imdb_id'].fillna('Unknown')
# logical fill
title["seasons"] = title["seasons"].fillna(0)

# numeric fill
title['imdb_score'] = title['imdb_score'].fillna(title['imdb_score'].median())
title['imdb_votes'] = title['imdb_votes'].fillna(0)
title['tmdb_popularity'] = title['tmdb_popularity'].fillna(title['tmdb_popularity'].median())
title['tmdb_score'] = title['tmdb_score'].fillna(title['tmdb_score'].median())
print("credits.csv")
print(credit.isnull().sum())
# logical fill
credit["character"] = credit["character"].fillna("Unknown")

# Fix data type 
title['release_year'] = title['release_year'].astype(int)
title['imdb_score'] = title['imdb_score'].astype(float)
title['imdb_votes'] = title['imdb_votes'].astype(float)
title['tmdb_score'] = title['tmdb_score'].astype(float)
title['tmdb_popularity'] = title['tmdb_popularity'].astype(float)

# clean list column 
title['genres'] = title['genres'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
title['production_countries'] = title['production_countries'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
title = title.explode('genres')
title = title.explode('production_countries')
title['production_countries'] = title['production_countries'].str.strip()

# mapping country
import pycountry

def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return None

title['country_name'] = title['production_countries'].apply(get_country_name)

# fill text (country)
title['production_countries'] = title['production_countries'].fillna('Unknown')
title['country_name'] = title['country_name'].fillna('Unknown')
title['genres'] = title['genres'].fillna('Unknown')


# remove duplicate 
title = title.drop_duplicates()
credit = credit.drop_duplicates()

# Clean Credits Data 
actor = credit[credit['role'] == 'ACTOR']
director = credit[credit['role'] == 'DIRECTOR']
credit = credit.dropna(subset=['name'])

# merge data 
merged = title.merge(credit, on='id', how='left')

# outlier dertection 
title = title[title['imdb_score'] <= 10]
title = title[title['tmdb_score'] <= 10]
title = title[title['runtime'] > 0]

# Standardize text 
title['title'] = title['title'].str.strip()
title['title'] = title['title'].str.lower()

# New column
title['content_age'] = 2026 - title['release_year']
title['avg_score'] = (title['imdb_score'] + title['tmdb_score']) / 2



# Export #
title.to_csv("title_country.csv", index=False)
credit.to_csv("credit_cleaned.csv", index=False)

# check
print("check")
print(title.isnull().sum())
print(credit.isnull().sum())


