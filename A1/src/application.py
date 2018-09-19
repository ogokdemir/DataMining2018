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
  

dat = read_and_process_file("C:\\Users\\Ozan Gokdemir\\Desktop\\DataMining2018\\A1\\data\\sorted.csv")    

#print(len(dat))


#finds the single item candidates in the dataset. 
def findCandidates1(dataset):
    print("first candidates are being found")
    cands = []
    for trans in dataset: 
        for item in trans:
            if not {item} in cands:
                cands.append({item})
    
    cands.sort()
    #returning frozensets so that these itemsets can be used as the keys of a dictionary(a.k.a python hashtable).
    return list(map(frozenset, cands))
    
    
#print(len(findCandidates1(dat)))
#print(findCandidates1(dat))

#an attempt to optimize the the algorithm. 
#idea is that a transaction that does not contain any frequent k-itemset is useless in subsequent scans.
def transaction_reduction(frequentItemsets, dataset):
    print("transaction_reduction called")
    for trans in dataset:
        for freqSet in frequentItemsets:
            if freqSet.issubset(trans):
                break
        dataset.remove(trans)


#filters the candidates that satisfy the support requirement, keeps the valid ones and dumps the rest. 
def findFrequentItemsets(cands, dataset, supCriteria):
    print("findfrequentitemsets called.")
    frequentItemsets = [] #stores only the candidates that satisy the support threshold. 
    while(len(cands)>0):
        temp = []
        for c in cands: 
            if support(c, dataset) >= supCriteria:
                temp.append(frozenset(c))
                frequentItemsets.append(c)
        before_removal = len(dataset)        
        transaction_reduction(frequentItemsets, dataset)
        after_removal = len(dataset)
        print("transaction reduction executed, " + str(before_removal - after_removal)+ "transactions removed.")
        print(str(after_removal) + " transactions remaining.")
        cands = []
        
        for t in temp:
            temp.remove(t)
            for u in range(len(temp)):
                miniset = frozenset(temp[u].union(t))
                cands.append(miniset)
    return frequentItemsets


def support(itemset, dataset):
    count = 0 
    for trans in dataset:
        if itemset.issubset(trans):
            count += 1
    return count



def confidence(precedent, antecedent, database):  
    testset = precedent.union(antecedent)
    
    return support(testset,database) / support(precedent, database)



def findRules(frequentItems, database, minConfidence):
    
    rules = {}
    
    for f in frequentItems:
        frequentItems.remove(f)
        for u in range(len(frequentItems)):
            conf = confidence(f, frequentItems[u], database)
            if conf >= minConfidence:
                if(len(f) <= len(frequentItems[u])):
                    rule = frozenset([f, frequentItems[u]])
                    rules[rule] = conf
    return rules
    

firstCandidates = findCandidates1(dat)

print("k1 candidates calculated, number is "+ str(len(firstCandidates)))

frequentItemsets = findFrequentItemsets(firstCandidates, dat, 170)

print("frequent itemsets calculated, number is "+ str(len(frequentItemsets)))

rules = findRules(frequentItemsets, dat, 0.95)


for r in rules.keys():
    temp = list(r)
    print(str(temp[0]) + "===>" + str(temp[1]) + " with confidence= " + str(rules[r])+"\n")

print("rules calculated number is "+ str(len(rules)))
