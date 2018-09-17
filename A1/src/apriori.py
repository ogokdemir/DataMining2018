# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 16:46:39 2018

@author: Ozan Gokdemir
"""

import numpy as np

database = [frozenset([1, 3, 4]),frozenset ([2, 3, 5]), frozenset([1, 2, 3, 5]), frozenset([2, 5])]

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
        cands = []
        
        for t in temp:
            temp.remove(t)
            for u in range(len(temp)):
                miniset = frozenset(temp[u].union(t))
                cands.append(miniset)
    return frequentItemsets


#print(filterCandidates(findCandidates1(database), database, 0.5))



def support(itemset, dataset):
    
    #numAllTransactions = float(len(dataset)) # number of all transactions in the database.
    countOfAppearance = 0 
     
    for trans in dataset:
        if itemset.issubset(trans):
            countOfAppearance += 1
            
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
        
        
database2 = (frozenset([1,2,3]), frozenset([2,3]), frozenset([4,5]), frozenset([1,2]), frozenset([1,5]))
#out = findFrequentItemsets(database2, 2)
#print(out) #should print something containing sets {1},{2},{3},{5},{1,2}, and {2,3}.

#Should print something like {2} ===> {1,2}, {1} ===> {1,2}, {3} ===> {2,3}, and {2} === {2,3}
rules = list(findRules(database2, 0.5))
for r in rules:
    print(str(r[0]) + " ===> " + str(r[1]))



#print(findRules(database, 0.75))