from math import sqrt
import pandas as pd
import random as rand

#Importing the dataset as a pandas dataframe.
df = pd.read_csv("C:\\Users\\Ozan Gokdemir\\Desktop\\ozan_rain_tom\\A2\\data\\dataset.csv")

#Converting the data into a list of tuples for easier processing.
data = [tuple(x) for x in df.values]


#This stores the clusters we get at the end. It is the accumulator for our result.
clusterTree = []

#We're using the first n points in the data. Otherwise visualization gets messy.
#Also our algorithm is O(n^2), thus, it is unfeasible to execute it with 4k datapoints.
def sampleTheData(n):
    sample = []
    for i in range(n):
        sample.append(data[rand.randint(1,len(data))])
    
    return sample
    
sample = sampleTheData(100)



#We are using the Tree implementation that we imported from
#http://openbookproject.net/thinkcs/python/english3e/trees.html
class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left= left
        self.right = right
        
    def __str__(self):
        return str(self.cargo)
    
#This function is also imported from the link above.
def print_tree_indented(tree, level=0):
    if tree is None: return
    print_tree_indented(tree.right, level+1)
    print("<----" * level + str(tree.cargo))
    print_tree_indented(tree.left, level+1)

# Accepts two data points a and b.
# Returns the distance between a and b.
# Note that this might be specific to your data.
def calculateDistance(a,b):
    return sqrt((a[0]-b[0]  )**2 + (a[1]-b[1])**2)


#Finds the middle point of two centeroids.
def findCenteroid(a,b):
    x = (a[0] + b[0])/2
    y = (a[1] + b[1])/2
    
    return (x,y)

# Accepts two data points a and b.
# Produces a point that is the average of a and b.
def merge(a,b):
    root = findCenteroid(a.cargo, b.cargo)
    newTree = Tree(root, a, b)
    clusterTree.append(newTree)
    clusterTree.remove(a)
    clusterTree.remove(b)
    
    return 

'''
def traverseTree(tree):
    if tree is None: return 0
    listTree = []
    listTree.append(traverseTree(tree.left))
    listTree.append(traverseTree(tree.right))
    listTree.append(tree.cargo)
    while listTree[0] == 0:
        listTree.remove(0)
    
    #print(listTree)
    return listTree

def calculateRadius(cluster):
    radius = 0 
    listTree = traverseTree(cluster)
    for i in listTree[0:len(listTree) - 1]:
        print(cluster.cargo[0])
        print(cluster.cargo[1])
        print(i[0])
        #print(i[1])
        radius += sqrt((cluster.cargo[0]-i[0])**2 + (cluster.cargo[1]-i[0])**2)/(len(listTree))
    
    return radius
'''



# Accepts a list of data points.
# Produces a tree structure corresponding to a 
# Agglomerative Hierarchal clustering of D.
def HClust(D, k):
    for pair in D:
        clusterTree.append(Tree(pair))
    
    while len(clusterTree) != k:
        smallestDist = 1000000
        answer = []
        
        '''
        for i in range(len(clusterTree)):
            if calculateRadius(clusterTree[i]) > 65:
                break
        '''
        
        for firstPoint in clusterTree:
            for secondPoint in clusterTree:
                newDist = calculateDistance(firstPoint.cargo, secondPoint.cargo)
                if newDist == 0:
                    continue
                if newDist < smallestDist:
                    answer = [firstPoint, secondPoint]
                    
        merge(answer[0], answer[1])
        
        
    print("done")
    
    return
        
#testData = [(1,2), (3,4), (5,6)]

#We know our data should have 4 clusters
HClust(sample, 4)
for x in range(len(clusterTree)):
    print_tree_indented(clusterTree[x])

