#INF552
#Spring2017
#Assignment1-Decision Tree
#Group Member: Yu Hou; Haoteng Tang.



from math import sqrt
from math import exp
from math import pi
from math import log
import random

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from matplotlib import cm

#
# This method is used to get 2D point data from film and store them into a list
#
def getDataFromFile(filename):
    list = []
    f = open(filename, 'r')
    newLine = f.readline()          # get the first line

    while newLine:
        string = newLine[:-1]  # trim the " number"

        newRecord = string.split(",")  #split as ","
        newRecord[0] = float(newRecord[0])          #change the formation of the data.
        newRecord[1] = float(newRecord[1])
        list.append(newRecord)      #add a new record
        newLine = f.readline()          #next line

    return list

#
# This method is used to calculate the distance between two point.
#
def callDistance(x1,y1,x2,y2):
    distance = sqrt((x1-x2)**2 + (y1-y2)**2)        #calculate the distance of point(x1,y1) and point(x2,y2)
    return distance


#
# This method is used to calculate the centroid
#
def callMean(dict):

    x=0.0
    y=0.0
    for key,value in dict.items():
        x = x+value[0]
        y = y+value[1]
    x = x / len(dict)
    y = y / len(dict)
    return ([x,y])


#
# This method is used to check if this cluster is empty otherwise it can not calculate the centroid.
#
def whetherEmpty(dict):
    return (len(dict))

#
# This method is used to implement the K-means method
#
def kMeans(list):
    k=3
    go = True
    totalDistance = 0.0

    ok = True
    while ok:
        kList = []
        dict = {}
        for index in range(k):
            dict.setdefault(index, {})  # initial the dict to store the data
            # {1:{1:dis,2:dis}, 2:{3:dis, 4:dis},...}
            kList.append(random.randint(0, len(list) - 1))

        # dict = {0:{},1:{},2:{}}
        # kList = [13,119,119]

        for index in range(len(list)):
            number = 0
            smallest = callDistance(list[index][0], list[index][1], list[kList[0]][0],
                                    list[kList[0]][1], )
            for j in range(len(kList)):
                if smallest > callDistance(list[index][0], list[index][1], list[kList[j]][0],
                                           list[kList[j]][1], ):
                    smallest = callDistance(list[index][0], list[index][1], list[kList[j]][0],
                                            list[kList[j]][1], )
                    number = j
            dict[number].setdefault(index, list[index])
            totalDistance = totalDistance + smallest


        kList.clear()
        for key, value in dict.items():
            if whetherEmpty(value) ==0:

                ok = True
                break                   # meet empty dictionary, we should make ok as true and get new random initial case
            else:
                listIn = callMean(value)
                kList.append(listIn)
                ok =False


    # plt.title('K-means: Initial case')
    # for key,value in dict.items():
    #     if key == 0:
    #         for keyIn,valueIn in value.items():
    #             plt.scatter(valueIn[0], valueIn[1], marker='*', color='r')
    #     if key == 1:
    #         for keyIn,valueIn in value.items():
    #             plt.scatter(valueIn[0], valueIn[1], marker = '+',color ='g')
    #     if key == 2:
    #         for keyIn,valueIn in value.items():
    #             plt.scatter(valueIn[0], valueIn[1], marker = 'o',color = 'b')
    #
    # plt.show()



    count =0


    while go:
        dict.clear()
        for index in range(k):
            dict.setdefault(index, {})  # initial the dict to store the data
                                        # {1:{1:dis,2:dis}, 2:{3:dis, 4:dis},...}
        distance = 0.0
        for index in range(len(list)):
            number = 0
            smallest = callDistance(list[index][0], list[index][1], kList[0][0], kList[0][1], )
            for j in range(len(kList)):
                if smallest > callDistance(list[index][0], list[index][1], kList[j][0], kList[j][1], ):
                    smallest = callDistance(list[index][0], list[index][1], kList[j][0], kList[j][1], )
                    number = j
            dict[number].setdefault(index, list[index])

            distance = distance + smallest
        if distance >= totalDistance:
            go = False
        else:
            kList.clear()
            for key, value in dict.items():
                listIn = callMean(value)
                kList.append(listIn)
            count=count+1
            #print(count)
            totalDistance=distance



    plt.title('K-means: Result after several iteration')
    for key,value in dict.items():
        if key == 0:
            for keyIn,valueIn in value.items():
                plt.scatter(valueIn[0], valueIn[1], marker='*', color='r')
        if key == 1:
            for keyIn,valueIn in value.items():
                plt.scatter(valueIn[0], valueIn[1], marker = '+',color ='g')
        if key == 2:
            for keyIn,valueIn in value.items():
                plt.scatter(valueIn[0], valueIn[1], marker = 'o',color = 'b')

    plt.show()



    return totalDistance,kList

#...............................................................................................................#
# boundary. Above is K-means. bottom is GMM.
#...............................................................................................................#

#
# This method is used to calculate the mu.
#
def callMiu(list):
    miu = [[0.0,0.0],[0.0,0.0],[0.0,0.0]]           #miu is the mean of model1 model2 model3

    x = [0.0,0.0,0.0]                               #x is summation of x value for model1,2,3 with weight
    y = [0.0,0.0,0.0]                               #y is summation of x value for model1,2,3 with weight
    f = [0.0,0.0,0.0]                               #f is summation of weight for model1,2,3
    for index in range(len(list)):
        x[0] = x[0] + (list[index][0] * list[index][2])     #for model1
        x[1] = x[1] + (list[index][0] * list[index][3])      #for model2
        x[2] = x[2] + (list[index][0] * list[index][4])#for model3

        y[0] = y[0] + (list[index][1] * list[index][2])#for model1
        y[1] = y[1] + (list[index][1] * list[index][3])#for model2
        y[2] = y[2] + (list[index][1] * list[index][4])#for model3

        f[0] = f[0] + list[index][2]#for model1
        f[1] = f[1] + list[index][3]#for model2
        f[2] = f[2] + list[index][4]#for model3


    miu [0][0]= x[0]/f[0]
    miu [0][1]=y[0]/f[0]#for model1


    miu[1][0]= x[1] / f[1]
    miu[1][1]= y[1] / f[1]#for model2


    miu[2][0]= x[2] / f[2]
    miu[2][1]= y[2] / f[2]#for model3

    #miu = np.matrix(miu)
    return miu

#
# This method is used to calculate the sigma and amplitude.
#
def callSigmaNPii(list, miu):
    listNew = list
    f = [0.0, 0.0, 0.0]

    list = np.matrix(list)
    list = np.delete(list,[2,3,4],axis =1)          #delete the column2 column3 and column4

    summation1 = np.matrix('[0.0,0.0;0.0,0.0]')
    summation2 = np.matrix('[0.0,0.0;0.0,0.0]')
    summation3 = np.matrix('[0.0,0.0;0.0,0.0]')

    for index in range(len(list)):

        summation1 = summation1 + listNew[index][2]*((list[index] - miu[0]).getT()) * (list[index] - miu[0])        #getT() means get the transposition
        summation2 = summation2 + listNew[index][3]*((list[index] - miu[1]).getT()) * (list[index] - miu[1])
        summation3 = summation3 + listNew[index][4]*((list[index] - miu[2]).getT()) * (list[index] - miu[2])

        f[0] = f[0] + listNew[index][2]  # for model1
        f[1] = f[1] + listNew[index][3]  # for model2
        f[2] = f[2] + listNew[index][4]  # for model3



    sigma1 = summation1 / f[0]
    sigma2 = summation2 / f[1]
    sigma3 = summation3 / f[2]

    pii = [f[0],f[1],f[2]]





    return sigma1,sigma2,sigma3,pii


#
# This method is used to calculate the probability density function
#
def guassian(x,miu,sigam):
    x = np.matrix(x)
    x = np.delete(x, [2, 3, 4], axis=1)  # delete the column2 column3 and column4
    miu = np.matrix(miu)
    sigam = np.matrix(sigam)


    return (1/((2*pi)**(2/2))) *  (np.linalg.det(sigam)**(-1/2))  *  exp( -((x-miu)*(sigam**(-1))*((x-miu).getT()))/2 )

#
# This method is used to plot the result.
#
def plot_countour(x, y, z):

    xGrid = np.linspace(-4.1, 10.1, 100)
    yGrid = np.linspace(-4.1, 10.1, 100)  # define grid.
    zGrid = griddata((x, y), z, (xGrid[None, :], yGrid[:, None]), method='cubic')
    levels = [0.1, 0.4, 0.9, 1.6,]

    plt.contour(xGrid, yGrid, zGrid, len(levels), linewidths=0.5, colors='k', levels=levels)

    plt.contourf(xGrid, yGrid, zGrid, len(levels), cmap=cm.Blues_r, levels=levels)

    plt.colorbar()  # draw colorbar

    plt.scatter(x, y, marker='o', c='b', s=5)   # plot data points.


#
# This method is used to get the z value
#
def gauss(x, y, Sigma, mu):
    X = np.vstack((x, y)).T
    mat_multi = np.dot((X - mu[None, ...]).dot(np.linalg.inv(Sigma)), (X - mu[None, ...]).T)
    return np.diag(np.exp(-1 * (mat_multi)))

#
# This method is used to implement the GMM method
#
def gaussianMethod(list):

    ric = [0.0, 0.0, 0.0]

    for index in range(len(list)):
        m1= random.randint(0, 100)
        m2= random.randint(0, 100)
        m3= random.randint(0, 100)
        p1 = m1 / (m1+m2+m3)
        ric[0] = ric[0] + p1
        list[index].append(p1)
        p2 = m2 / (m1 + m2 + m3)
        ric[1] = ric[1] + p2
        list[index].append(p2)
        p3 = m3 / (m1 + m2 + m3)
        ric[2] = ric[2] + p3
        list[index].append(p3)

    miu = callMiu(list)                         #get miu
    sigma1,sigma2,sigma3,pii = callSigmaNPii(list,miu)  #get sigma

    #
    # x=[]
    # y=[]
    # for index in range(len(list)):
    #     x.append(list[index][0])
    #     y.append(list[index][1])
    #
    # z = gauss(x, y, Sigma=np.asarray(sigma1), mu=np.asarray(miu[0]))
    # plot_countour(x, y, z)
    # z = gauss(x, y, Sigma=np.asarray(sigma2), mu=np.asarray(miu[1]))
    # plot_countour(x, y, z)
    # z = gauss(x, y, Sigma=np.asarray(sigma3), mu=np.asarray(miu[2]))
    # plot_countour(x, y, z)
    # plt.show()



    go = True
    compare = 0.0


    count = 0
    while go:
        likeHood = 0.0
        for index in range(len(list)):
            a = pii[0] * guassian(list[index], miu[0], sigma1)
            b = pii[1] * guassian(list[index], miu[1], sigma2)
            c = pii[2] * guassian(list[index], miu[2], sigma3)
            summation = a + b + c
            list[index][2] = (a) / summation  # Ric1
            list[index][3] = (b) / summation  # Ric2
            list[index][4] = (c) / summation  # Ric3
            likeHood = likeHood + log(summation)

        miu = callMiu(list)  # get miu
        sigma1, sigma2, sigma3,pii = callSigmaNPii(list, miu)  # get sigma


        if compare==likeHood:
        #if count == 20:
            go = False
        else:
            compare = likeHood
        count = count +1
        # print(count)
        # print(compare)
        # print(miu)



    x=[]
    y=[]
    for index in range(len(list)):
        x.append(list[index][0])
        y.append(list[index][1])

    z = gauss(x, y, Sigma=np.asarray(sigma1), mu=np.asarray(miu[0]))
    plot_countour(x, y, z)
    z = gauss(x, y, Sigma=np.asarray(sigma2), mu=np.asarray(miu[1]))
    plot_countour(x, y, z)
    z = gauss(x, y, Sigma=np.asarray(sigma3), mu=np.asarray(miu[2]))
    plot_countour(x, y, z)
    plt.show()


    return compare,miu,sigma1,sigma2,sigma3,pii

if __name__ == '__main__':
    list = getDataFromFile("clusters.txt")

# ...............................................................................................................#
# run k-means 1 time.


    distance,miu = kMeans(list)
    print("The distance of this case "+str(distance))
    print("The centriod of each cluster ")
    print("The centriod of cluster 1:")
    print(miu[0][:])
    print("The centriod of cluster 2:")
    print(miu[1][:])
    print("The centriod of cluster 3:")
    print(miu[2][:])

# ...............................................................................................................#
# run k-means 100000 times.


    # bestDistance = 100000000.0
    # bestMiu = []
    # count =0
    # for index in range(100000):
    #     distance,miu = kMeans(list)
    #     if distance < bestDistance:
    #         bestMiu = miu
    #         bestDistance = distance
    #     count = count + 1
    #     print("Has already run "+str(count)+" times")
    # print("The distance of the best case "+str(bestDistance))
    # print("The centriod of each cluster ")
    # print(bestMiu)


# ...............................................................................................................#
# run GMM 1 time.


    likehood,miuG,sigma1,sigma2,sigma3,pii = gaussianMethod(list)
    print("The likelihood of this case: " + str(likehood))
    print("The mean of each Gaussian:")
    print("The first one: "+str(miuG[0]) + " The second one: "+str(miuG[1]) + " The third one: "+str(miuG[2]))
    print("The amplitude of each Gaussian:")
    print("The first one: "+str(pii[0]) + " The second one: "+str(pii[1]) + " The third one: "+str(pii[2]))
    print("The covariance matrix of each Gaussian:")
    print("The first one: " + str(sigma1) + "\nThe second one: " + str(sigma2) + "\nThe third one: " + str(sigma3))

# ...............................................................................................................#
# run GMM 1000 times. This will cost 10 hours.


    # bestLikehood = 0.0
    # bestMiuG = []
    # bestSigma = []
    # count =0
    # for index in range(1000):
    #     list = getDataFromFile("clusters.txt")
    #     likehood,miuG,sigma1,sigma2,sigma3 = gaussianMethod(list)
    #     if likehood > bestLikehood:
    #         bestMiuG = miuG
    #         bestSigma = [sigma1,sigma2,sigma3]
    #         bestLikehood = likehood
    #     print(count)
    #     count=count+1
    # print(bestLikehood)
    # print(bestMiuG)
    # print(bestSigma)




