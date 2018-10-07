
#A template for the implementation of K-Means.

from math import sqrt
import pandas as pd
import random as rand

#Importing the dataset as a pandas dataframe.
df = pd.read_csv("C:\\Users\\Ozan Gokdemir\\Desktop\\ozan_rain_tom\\A2\\data\\dataset.csv")


# Accepts two data points a and b.
#Returns the euclidian distance 
#Since the data has only two feautures, I represent a and b as tuples.
# between a and b.
def euclidianDistance(a,b):
    return sqrt((float(a[0])-float(b[0]))**2 + (float(a[1])-float(b[1]))**2)


def generateInitialRandomCenteroids(k):
    initial_centeroids = []
    #We'll create k centeroids.
    for i in range(k):    
        #x-axis value (distance) of the first random centeroid.
        randx = rand.randint(0, int(max(df["Distance"])))
        #y-axis value(speeding) of the first random centeroid.
        randy = rand.randint(0, int(max(df["Speeding"])))
        initial_centeroids.append((randx, randy))
    
    #Return a list of tuples. Each tuples represents the "coordinates" of a centeroid. 
    #Since there are only two features, tuple is plausible here.    
    return initial_centeroids

#print(generateInitialRandomCenteroids(4))


# Accepts a list of data points D, and a list of centers
# Returns a dictionary of lists called "clusters", such that
# clusters[c] is a list of every data point in D that is closest
#  to center c.
    

def assignClusters(D, centers):
    #all clusters are initially empty and num of clusters = num of centers.
    #Clusters is a dictionary of lists: Keys are centeroids(tuples) and values are a lists containing
    #the pandas dataframe rows.
    clusters = {i:[] for i in centers}
    
    #Loop through all the datapoints in the cluster.
    for i in range(len(D)):
        #For each data point, a temporary dictionary mapping the point's distance to each centeroid.
        dist_to_centers = {}
        #for each centeroid
        for candidate_centeroid in centers:
            #put the distance b/w the centeroid and data point into the dictionary.
            dist_to_centers[candidate_centeroid]= euclidianDistance((D.iloc[i][0], D.iloc[i][1]), candidate_centeroid)
        
        #The closest centeroid is the key with the minimum value in the dist_to_centers dictionary.
        closest_center = min(dist_to_centers, key = dist_to_centers.get)
        #Put the data point into the cluster. Namely, to the list of the centeroid in the dictionary.
        clusters[closest_center].append((D.iloc[i]))
        
    
    return clusters



#Accepts a list of data points.
#Returns the mean of the points.
def findClusterMean(cluster):
    sumDistance = 0 
    sumSpeeding = 0 
    
    for row in cluster:
        sumDistance += row["Distance"]
        sumSpeeding += row["Speeding"]
    
    avgDistance = sumDistance/len(cluster)
    avgSpeeding = sumSpeeding/len(cluster)
    
    return((avgDistance, avgSpeeding))
    
'''
findClusterMean Test

clusters = assignClusters(df, generateInitialRandomCenteroids(4))    
for k,v in clusters.items():
    print(findClusterMean(v))

'''

def sumOfInClusterDistances(center, cluster):
    sumDistance = 0 
    for row in cluster: 
        sumDistance += sqrt((center[0]-row["Distance"])**2 + center[1]-row["Speeding"])
        
    
def calculateInertia(clusters):
    inertia = 0 
    for center, cluster in clusters.items():
        for datapoint in cluster:
            inertia += sqrt((center[0]-datapoint["Distance"])**2 + 
                            (center[1]-datapoint["Speeding"])**2)
    
    return inertia

'''Inertia Testing
x=  calculateInertia(assignClusters(df, generateInitialRandomCenteroids(4)))
print(x)

'''
            
# Accepts a list of data points, and a number of clusters.
# Produces a set of lists representing a K-Means clustering
#  of D.




def KMeans(D, k):
    #Initial centers.
    centers = generateInitialRandomCenteroids(k)
    
    #Initial clustering with the random centers.
    clusters = assignClusters(D, centers)
    
    #Calculate the initial inertia.
    inertia = calculateInertia(clusters)
    
    #A list to keep track of the inertia improvement in each clustering step.
    #Stores the difference between inertia from a step and the one before.
    inertiadiff = []
    
    #Emulating the deprecated do-while loop because it is what I need here.
    while True:
        #Stores the new centeroids calculated at each step.
        newCenters = []
        #Loop through the current clusters, find their medians and store in the newCenters array.
        for k,v in clusters.items():
            newCenters.append(findClusterMean(v))
        
        #Compute the new clusters from the new centers calculated from the previous clusters.
        clusters = assignClusters(df, newCenters)
        #Compute the new inertia.
        newInertia = calculateInertia(clusters)
        #Compute the difference between the inertia of previous cluster and this one, store the value.
        inertiadiff.append(inertia - newInertia)
        
        #If the change in the inertia hits zero, this means the data points don't move between 
        #clusters anymore. Thus, break the loop.
        if(inertia-newInertia == 0.0):
            break
        
        #New inertia is the old inertia now, because the loop will compute a newInertia next.
        inertia = newInertia
        
    return clusters


 
cls = KMeans(df, 4)
for k,v in cls.items():
    print(len(v))
    


