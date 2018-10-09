#A template for the implementation of K-Medoids.
from math import sqrt
import pandas as pd
import random as rand

#Importing the dataset as a pandas dataframe.
df = pd.read_csv("C:\\Users\\Ozan Gokdemir\\Desktop\\ozan_rain_tom\\A2\\data\\dataset.csv")

#Converting the data into a list of tuples for easy processing.
data = [tuple(x) for x in df.values]




# Accepts two data points a and b.
# Returns the distance between a and b.
# Note that this might be specific to your data.

#Always pass the center(tuple) in a, pandas df row in b. 
def calculateDistance(a,b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)




# Accepts a list of data points D, and a list of centers
# Returns a dictionary of lists called "clusters", such that
# clusters[c] is a list of every data point in D that is closest
#  to center c.
# Note: This can be identical to the K-Means function of the same name.
def assignClusters(D, centers):
    #all clusters are initially empty and num of clusters = num of centers.
    #Clusters is a dictionary of lists: Keys are centeroids(tuples) and values are a lists containing
    #the pandas dataframe rows
    clusters = {i:[] for i in centers}
    
    #Loop through all the datapoints in the cluster.
    for i in range(len(D)):
        #For each data point, a temporary dictionary mapping the point's distance to each centeroid.
        dist_to_centers = {}
        #for each centeroid
        for candidate_centeroid in centers:
            #put the distance b/w the centeroid and data point into the dictionary.
            dist_to_centers[candidate_centeroid]= calculateDistance(D[i], candidate_centeroid)
        
        #The closest centeroid is the key with the minimum value in the dist_to_centers dictionary.
        closest_center = min(dist_to_centers, key = dist_to_centers.get)
        #Put the data point into the cluster. Namely, to the list of the centeroid in the dictionary.
        clusters[closest_center].append((D[i]))
        
    return clusters



def generateInitialRandomCenteroids(k):
    initial_centeroids = []
    #We'll create k centeroids.
    for i in range(k):    
        #x-axis value (distance) of the first random centeroid.
        randx = rand.randint(0, int((max(x[0] for x in data))))
        #y-axis value(speeding) of the first random centeroid.
        randy = rand.randint(0, int(max(x[1] for x in data)))
        initial_centeroids.append((randx, randy))
    
    #Return a list of tuples. Each tuples represents the "coordinates" of a centeroid. 
    #Since there are only two features, tuple is plausible here.    
    return initial_centeroids



# Accepts a list of data points.
# Returns the medoid of the points.
def findClusterMedoid(center, cluster):
     for cand in cluster:
        dist_center = 0
        dist_cand = 0
        for datapoint in cluster:
            dist_center += calculateDistance(center, datapoint)
            dist_cand += calculateDistance(cand, datapoint)
        if dist_cand < dist_center:
            return cand
        else:
            return center

# Accepts a list of data points, and a number of clusters.
# Produces a set of lists representing a K-Medoids clustering
#  of D.
def KMedoids(D, k):
    centers = generateInitialRandomCenteroids(k)
    #newMedioid = 0 # dummy initial
    
    while True:
        newCenters = []
        clusters = assignClusters(D, centers)
    
        for center, cluster in clusters.items():
            tempCenter = center
            #if (findClusterMedoid(tempCenter, cluster) == center):
            newCenters.append(findClusterMedoid(tempCenter, cluster))
        
        if(centers == newCenters):
            #Break here.
            return assignClusters(D, centers)
        
        
        centers = newCenters
        

test = KMedoids(data, 4)
for k,v in test.items():
    print(len(v))




