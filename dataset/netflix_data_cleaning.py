# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 23:12:07 2026

@author: Tongtaffle
"""

import pandas as pd

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
credit = credit["character"].fillna("Unknown")
print(credit.isnull().sum())
