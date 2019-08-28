#INF552
#Spring2017
#Assignment3-PCA and Fastmap
#Group Member: Yu Hou; Haoteng Tang.

from math import sqrt

import random

import numpy as np
from numpy.linalg import eig

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



#
# This method is used to get 2D point data from film and store them into a list
#
def getDataFromFile(filename):
    list = []
    f = open(filename, 'r')
    newLine = f.readline()          # get the first line

    while newLine:
        string = newLine[:-1]  # trim the " number"

        newRecord = string.split("\t")  #split as ","
        newRecord[0] = float(newRecord[0])          #change the formation of the data.
        newRecord[1] = float(newRecord[1])
        newRecord[2] = float(newRecord[2])
        list.append(newRecord)      #add a new record
        newLine = f.readline()          #next line

    return list

def callMiu(list):
    miu=[0.0,0.0,0.0,]
    for index in range(len(list)):
        miu[0] = miu[0] + list[index][0]
        miu[1] = miu[1] + list[index][1]
        miu[2] = miu[2] + list[index][2]
    miu[0] = miu[0] / len(list)
    miu[1] = miu[1] / len(list)
    miu[2] = miu[2] / len(list)

    return miu
def callSigma(miu,list):
    newList = list
    for index in range (len(list)):
        newList[index][0] = list[index][0] - miu[0]
        newList[index][1] = list[index][1] - miu[1]
        newList[index][2] = list[index][2] - miu[2]

    newList = np.matrix(newList)
    sigma = (newList.getT() * newList) / (len(list))

    return sigma
def callU(sigma):
    v = eig(sigma)[1]       #[0] is eigevalue, [1] is eigevector
    u = np.delete(v, [2], axis=1)
    #print(u)
    return u

def callZ(u,list):
    list = np.matrix(list)
    u = np.matrix(u)
    #print(u)
    z = ( u.getT() * list.getT() ).getT()
    #print(z)
    return z

def methodPCA(list):
    miu = callMiu(list)
    sigma = callSigma(miu,list)
    u = callU(sigma)

    zlist = callZ(u,list)
    return zlist

def drawlist(list):

    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, projection='3d')
    for index in range(len(list)):
        ax.scatter(list[index][0], list[index][1], list[index][2],
               marker='o', color='blue', s=1)


    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.title("6000 points in 3D view")
    plt.show()

def drawZList(zList):

    x = np.delete(zList, [1], axis=1)
    y = np.delete(zList, [0], axis=1)

    for index in range(len(zList)):
        print("wait")
        plt.scatter(x[index], y[index], s=1, marker='o', color='b')
    plt.show()

#...............................................................................................................#
# boundary. Above is PCA. below is fastMap.
#...............................................................................................................#

def getDataFromFile2(filename):
    dict = {}

    f = open(filename, 'r')
    newLine = f.readline()          # get the first line

    while newLine:
        string = newLine[:-1]  # trim the " number"

        newRecord = string.split("\t")  #split as ","
        newRecord[0] = float(newRecord[0])          #change the formation of the data.
        newRecord[1] = float(newRecord[1])
        newRecord[2] = float(newRecord[2])

        if newRecord[0] not in dict:
            dict.update( {newRecord[0]: {newRecord[1]:newRecord[2]} })
        else:
            dict.get(newRecord[0]).update({newRecord[1]:newRecord[2]})

        if newRecord[1] not in dict:
            dict.update( {newRecord[1]: {newRecord[0]:newRecord[2]} })
        else:
            dict.get(newRecord[1]).update({newRecord[0]:newRecord[2]})


        newLine = f.readline()          #next line

    return dict

def callTri(a,b,distance,dict):
    map = {}
    for key,value in dict.items():
        if key==a:
            map.update({a:0.0})
        elif key == b:
            map.update({b:distance})
        else:
            dis= (dict[a][key]**2 + dict[a][b]**2 - dict[key][b]**2) / (2*dict[a][b])
            map.update({key:dis})

    return map

def callDict(mapX,dict):
    dict2 = {}
    for i in range( 1,len(dict)+1):
        i=float(i)
        dict2.update({i:{}})
        for j in range(1,len(dict)+1):
            j=float(j)
            if i ==j :
                continue
            else:
                number1 = sqrt( (dict[i][j])**2 - (mapX[i]-mapX[j])**2 )
                dict2[i].update({j : number1})


    return dict2
def callAB(dict):
    number1 = random.randint(1, len(dict))
    bestdistance = 0.0

    for key, value in dict.items():
        if value == dict[number1]:
            a = key

    for key, value in dict[number1].items():
        if value > bestdistance:
            bestdistance = value
            b = key

    go = True
    while go:
        c = 0.0

        for key, value in dict[b].items():
            if value > bestdistance:
                bestdistance = value
                c = key
        if c == 0.0:
            go = False
        else:
            a = b
            b = c
    if a>b:
        c = a
        a = b
        b = c

    return (a,b,bestdistance)
def printMatrix(mapX,mapY):

    matrix = [[]]
    matrix = [[0.0 for x in range(2)] for y in range(10)]

    for index in range(len(mapX)):
        matrix[index][0] = mapX[float(index)+1.0]
        matrix[index][1] = mapY[float(index)+1.0]
    matrix = np.matrix(matrix)
    print(matrix)

def methodFastmap(dict):
    a,b,bestdistance=callAB(dict)


    mapX = callTri(a,b,bestdistance,dict)
    dict2 = callDict(mapX,dict)

    a,b,bestdistance=callAB(dict2)
    mapY = callTri(a,b,bestdistance,dict2)
    printMatrix(mapX,mapY)

    n = ['acting', 'activist',
         'compute', 'coward',
         'forward',
         'interaction',
         'activity',
         'odor',
         'order',
         'international']


    fig, ax = plt.subplots()
    for index in range(1, len(mapX) + 1):
        ax.scatter(mapX[index], mapY[index], marker='*', color='r')
        ax.annotate(n[index-1],(mapX[index], mapY[index]))
    plt.show()



if __name__ == '__main__':
    list = getDataFromFile("pca-data.txt")

    # drawlist(list)            #draw the 3D list. SLOW!!!


    zList=methodPCA(list)           # PCA methond
    out = open("PCA.txt",'w')     # output of the resutl.
    for item in zList:
        #print(item)
        out.write(str(item))
        out.write("\n")
        # out.write(str(item))
        # out.write("\n")
    print(zList)
    # # drawZList(zList)              # draw the 2D list.



    # dict = getDataFromFile2("fastmap-data.txt")         #fastmap method.
    # methodFastmap(dict)


