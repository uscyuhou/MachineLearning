

from math import log



#
# This function is used to get the database from the file
#
def creatDatabaseFromFile(filename):
    f = open(filename,'r')
    string = f.readline()           #get the first line
    string = string.replace(" ","") #trim the " "
    string = string[1:-2]           #trim the "(",")"and"\n"
    attribute=string.split(",")     #get the atrribut list
    emptyLine = f.readline()        #delete the empty line
    database = []
    newLine = f.readline()

    while newLine:
        if newLine[-1] == '\n':
            string = newLine[3:-2]  # trim the " number"
        else:
            string = newLine[3:-1]          #trim the " number"

        string = string.replace(" ", "")#trim the " "
        newRecord = string.split(",")   #split as ","
        database.append(newRecord)      #add a new record
        newLine = f.readline()          #next line

    return database, attribute
#
# This function is used to divide the original database into different sub-database with different
# value of original database.
#

def divideTheDatabase(database, choosedAttribute, value):
    subdatabase = []
    for vector in database:
        if vector [choosedAttribute] == value:
            subdatabase.append(vector)          #get the sub-database which are fit into the choosed attribute.

    return subdatabase



#
# get the entropy of current database with different attribute.
#
def getEntropy(database,checkingAttribute):
    enjoy = 7
    avgEntopy=0
    logBase = 2
    totalNumber = 0
    values = {}
    for vector in database:
        value = vector [checkingAttribute]
        if len(values) == 0 or value not in values.keys():
            values.update({value : {}})

        if vector [enjoy] not in values [value].keys():
            values [value].update({vector[enjoy]: 1})
        else:
            number = values [value][vector[enjoy]]
            values[value][vector[enjoy]] = number +1
        totalNumber = totalNumber +1

    for key,value in values.items():
        sumNumber=0
        if ('Yes' not in value) or ('No' not in value) or (value['Yes']==0) or (value['No']==0):           # if the yes or no = 0, we can not calculate the entropy.
            entropy =0
            value.update({'entropy': entropy})  # calculate each entropy
        else:
            sumNumber = value['Yes'] + value['No']
            value.update({'sum': sumNumber})
            entropy = ((value['Yes'] / sumNumber) * log(sumNumber / value['Yes'], logBase)) + \
                      ((value['No'] / sumNumber) * log(sumNumber / value['No'], logBase))
            value.update({'entropy': entropy})  # calculate each entropy
        avgEntopy = avgEntopy + ((sumNumber / totalNumber) * entropy)  # calculate the avg entropy


    return avgEntopy

#
# This function is used to get a list in which there are all values of a attribute.
#
def getValues(database,checkingAttribute,data):
    enjoy = 7
    values = {}
    for vector in database:
        value = vector[checkingAttribute]

        if len(values) == 0 or value not in values.keys():
            values.setdefault(value)
            values[value] = vector[enjoy]

    for vector in data:
        value = vector[checkingAttribute]
        if value not in values.keys():
            values[value]= 'tie'    # if this value is not in values list, give it tie.

    return values




#
# This function is the core function
# In this function, we can divide a tree by some criterion
# Return a decision tree stored by the dictionary.
#
def getDecisionTree(database, attribute,data):
    enjoy = 7

    bestAtrributeNumber = 0
    bestEntropy = 1.0
    for index in range(len(attribute)-2):
        getE = getEntropy(database, index)
        if bestEntropy > getE:
            bestEntropy = getE
            bestAtrributeNumber = index

    myTree = {}
    if len(database)==0:                                # In this situation, we give it tie
        myTree.setdefault(value, {})
        myTree[value].update('tie')
        return myTree

    if bestEntropy == 0.0:                              # In this situation, we give it yes or no or go on divide the tree.
        result= 'Yes'
        count = 0
        for vector in database:
            value = vector[enjoy]
            if result == value:
                count=count+1
        if count==0:
            myTree = 'No'
        elif count == len(database):
            myTree = 'Yes'
        else:
            myTree.setdefault(attribute[bestAtrributeNumber], {})
            myTree[attribute[bestAtrributeNumber]].update(getValues(database,bestAtrributeNumber,data))

        return myTree


    values = []
    for vector in data:
        value = vector[bestAtrributeNumber]
        if len(values) == 0 or value not in values:
            values.append(value)



    myTree.setdefault(attribute[bestAtrributeNumber],{})
    for index in range(len(values)):
        myTree[attribute[bestAtrributeNumber]].update({values[index]:getDecisionTree(divideTheDatabase(database, bestAtrributeNumber, values[index]),attribute,data)})


    return myTree

#
# In order to print this decision tree, we need to change the dictionary to a list.
#
def dictToList(myTree,list,number):
    if type(myTree)!=dict:
        list[number].append(myTree)
        return list
    if len(list)<=number+1:
        list.append([])
    for key,value in myTree.items():

        list[number].append(key)
        dictToList(value,list,number+1)
    return list
#
# This function is used to print the decision tree.
#
def printDT(list):
    for i in range(len(list)):
        if i % 2 == 0:
            for j in range(len(list[i])):
                if j==len(list[i])-1:
                    print(list[i][j], end="")
                else:
                    print(list[i][j],end=",")
            print()



if __name__ == '__main__':
    database, attribute = creatDatabaseFromFile("dt-data.txt")
    myTree=getDecisionTree (database, attribute,database)
    #print(myTree)
    list = [[]]
    list=dictToList(myTree,list,0)
    #print(list)

    print("Print out decision tree:")
    printDT(list)


