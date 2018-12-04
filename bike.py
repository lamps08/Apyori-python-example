# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 12:20:04 2018

@author: Mnaumani
"""
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from apyori import apriori  

df = pd.read_csv("C:\\Users\\mnaumani\\Desktop\\New folder\\side\\bakery\\Breakfast.csv")

df['transdate'] =  pd.to_datetime(df['Date']+df['Time'], format='%Y-%m-%d%H:%M:%S')

# Exploratory Analysis

item_frequency = df.groupby('Item')['Date'].count().sort_values(ascending = False).reset_index()
item_frequency['relative_freq'] = item_frequency.Date/item_frequency.Date.sum()
sns.barplot(x = 'Item', y = 'Date',data = item_frequency.head(6))
sns.barplot(x = 'Item', y = 'relative_freq',data = item_frequency.head(6))


# Making the Dataset in format for use with apriori algorithm 
df.drop(['Date', 'Time'], axis = 1, inplace = True)
df['sum_trans'] = df.transdate.map(str) +"&"+ df.Transaction.map(str)
#thanks to stack overflow 
item_sets = df.groupby('sum_trans')['Item'].apply(lambda x: "%s" % ','.join(x)).reset_index()
item_sets['Date'], item_sets['Transaction'] = item_sets['sum_trans'].str.split('&', 1).str
item_sets.drop('sum_trans', axis = 1, inplace = True)
item_sets_list = item_sets['Item'].tolist()
# change to list of list
item_sets_l = [str(i).split(',') for i in item_sets_list]


# Run Apriori Model
support = [0.005,0.0010,0.01,0.02]

confidence = [0.1,0.3,0.5,0.7]

results_l = []
for i in range(len(support)):
    for j in range(len(confidence)):
        rules = apriori(item_sets_l, min_support = support[i], min_confidence =  confidence[j], min_lift = 1, min_length = 2)
# the results
        results = list(rules) 
        results_l.append(len(results))
        
        print ("support is {}, confidence is {}".format(support[i], confidence[j]))
        print ("Number of rules are {}".format(len(results)))
         
#print (results)
#Make the output easier to understand
rules = apriori(item_sets_l, min_support = 0.005, min_confidence =0.3 , min_lift = 1.1, min_length = 2)
# the results
results = list(rules)   

def make_pretty(lst):
    for rule in lst:
        
        itemsets1 = list(str(rule[0]).split('\''))
        for i in itemsets1:
            if ")" not in i and "(" not in i and ',' not in i:
                
                print (i,"-->")          
        #itemset1 = str(rule[0]).split('\'')[1]
        #itemset2 = str(rule[0]).split('\'')[3]  
        support = rule[1]
        confidence =str( rule[2]).split(',')[2]  
        lift = str( rule[2]).split(',')[3].strip('])') 
        n1=  '\n'
        print ("{} Support = {},{},{}".format(n1,support, confidence, lift))
print (make_pretty(results))