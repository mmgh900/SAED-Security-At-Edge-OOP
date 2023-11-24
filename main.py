#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 23:52:57 2020

@author: zobaed
"""
import gensim

from Units.ContextDetectionUnit import ContextDetectionUnit
from Units.QueryExpansionUnit import QueryExpansionUnit
from Units.WeightingUnit import WeightingUnit

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 23:53:55 2020

@author: zobaed
"""

import configparser

import enchant

# Import the enchant library and create a dictionary for US English
engcheker = enchant.Dict("en_US")

# Import the configparser library and create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Get the query from the DEFAULT section of the configuration file
query = config['DEFAULT']['query']

# Assign the query to the variable sent
Q = query

'''    Content Detection         '''
cdu = ContextDetectionUnit()
C, C_clustered, Q_prime, N = cdu.get_context(Q)


# Load the pre-trained word embeddings model
model = gensim.models.KeyedVectors.load_word2vec_format(config['DEFAULT']['google_news_link'], binary=True)


'''    Expansion         '''
qeu = QueryExpansionUnit(model)
P = qeu.expand_query(Q, C)

'''
Weight Distribution 
'''
wu = WeightingUnit(config['DEFAULT']['interest'], model)
combined_dict = wu.weight_keywords(C_clustered, Q_prime, N, Q, P)

'''For Java Program'''
ac = str(combined_dict)
acc = ac.split(",")
f = open("./Weighted_query_" + Q + ".txt", "w")

for i in acc:
    if ',' in i:
        i = i.replace(',', '')

    if '{' in i:
        i = i.replace("{", '')

    if "}" in i:
        i = i.replace("}", '')

    if "'" in i:
        i = i.replace("'", '')

    if " " in i[0]:
        i = i[1:]

    if " " in i[i.index(":") + 1]:
        i1 = i[: i.index(":") + 1]
        i2 = i[i.index(":") + 1:]
        i = i1 + i2

    if "-" in i:
        i = i.replace("-", "")

    f.write(i)
    print(i)
    f.write("\n")

f.close()
