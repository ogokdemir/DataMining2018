# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 21:07:16 2018

@author: Ozan Gokdemir
"""

#a function to read the csv, generate lists of movies for each user. 

import csv 

def read_and_process_file(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_users_movie_list = []
        database = []
        current_user = 0
        for row in reader:
            if row[0] == current_user:
                current_users_movie_list.append(row[1])
            else:
                database.append(current_users_movie_list)
                current_user = row[0]
                current_users_movie_list = [row[1]]
                
         
    del database[0:2]
    return list(map(frozenset,database))
    
data = read_and_process_file('C:\\Users\\Ozan Gokdemir\\Desktop\\DataMining2018\\A1\\data\\sorted.csv')
          
    

#finds the single item candidates in the dataset. 
def findCandidates1(dataset):
    cands = []
    for trans in dataset: 
        for item in trans:
            if not [item] in cands:
                cands.append([item])
    
    cands.sort()
    #returning frozensets so that these itemsets can be used as the keys of a dictionary(a.k.a python hashtable).
    return list(map(frozenset, cands))
    
    
#print(findCandidates1(database))


#an attempt to optimize the the algorithm. 
#idea is that a transaction that does not contain any frequent k-itemset is useless in subsequent scans.
def transaction_reduction(frequentItemsets, dataset):
    for trans in dataset:
        count = 0 
        for freqSet in frequentItemsets:
            if freqSet.issubset(trans):
                count+=1 
        if count == 0:
            dataset.remove(trans)


#filters the candidates that satisfy the support requirement, keeps the valid ones and dumps the rest. 
def findFrequentItemsets(dataset, supCriteria):
    frequentItemsets = [] #stores only the candidates that satisy the support threshold. 
    cands = findCandidates1(dataset)
    while(len(cands)>0):
        temp = []
        for c in cands: 
            if support(c, dataset) >= supCriteria:
                temp.append(frozenset(c))
                frequentItemsets.append(c)             
        transaction_reduction(frequentItemsets, dataset)
        cands = []
        
        for t in temp:
            temp.remove(t)
            for u in range(len(temp)):
                miniset = frozenset(temp[u].union(t))
                cands.append(miniset)
    return frequentItemsets




#print(filterCandidates(findCandidates1(database), database, 0.5))


supportCache = {}

def support(itemset, dataset):
    
    if(itemset in supportCache):
        return supportCache[itemset]
    else:
        countOfAppearance = 0  
        for trans in dataset:
            if itemset.issubset(trans):
                countOfAppearance += 1
        
        supportCache[itemset] = countOfAppearance
        return countOfAppearance

def confidence(precedent, antecedent, database):  
    testset = precedent.union(antecedent)
    return support(testset,database) / support(precedent, database)


def findRules(database, minConfidence):
    frequentItems = findFrequentItemsets(database, 2)
    rules = []
    
    for f in frequentItems:
        frequentItems.remove(f)
        for u in range(len(frequentItems)):
            if confidence(f, frequentItems[u], database) >= minConfidence:
                if(len(f) <= len(frequentItems[u])):
                    rules.append((f , frequentItems[u]))
    return rules
    

rules = list(findRules(data, 0.5))
for r in rules:
    print(str(r[0]) + " ===> " + str(r[1]))
    
    