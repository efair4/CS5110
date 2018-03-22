import graphviz as gv
import random
import math
import copy
from random import shuffle

CANDIDATES = ['Highest','High','Medium','Low','Lowest']
AGENTS = ['A','B','C','D','E']
HIGHESTWEIGHT = 6

def main():
    #userPref = getUserPref()
    randomPref = getRandPref()
    oneHigherPref = getOneHigherPref()
    sameWeightPref = getSameWeightPref()

    #The following hold the majority graph data for each voting method
    #userMajority = getMajority(userPref)
    randMajority = getMajority(randomPref)
    oneHigherMajority = getMajority(oneHigherPref)
    sameWeightPrefMajority = getMajority(sameWeightPref)

    #userGraphStuff = getGraph(userMajority, 'user')
    randDegreeList = getGraph(randMajority, 'rand')
    oneHigherDegreeList = getGraph(oneHigherMajority, 'oneHigher')
    sameWeightPrefDegreeList = getGraph(sameWeightPrefMajority, 'sameWeightPref')



    #userBorda = bordaOrder(userPref)
    randBorda = bordaOrder(randomPref)
    oneHigherBorda = bordaOrder(oneHigherPref)
    sameBorda = bordaOrder(sameWeightPref)

    #userSecondCopeland = secondCopelandOrder(userPref)
    randSecondCopeland = secondCopelandOrder(randomPref)
    oneHigherSecondCopeland = secondCopelandOrder(oneHigherPref)
    sameSecondCopeland = secondCopelandOrder(sameWeightPref)

    #userSTV = stvOrder(userPref)
    randSTV = stvOrder(randomPref)
    oneHigherSTV = stvOrder(oneHigherPref)
    sameSTV = stvOrder(sameWeightPref)

    #makeTable('User Choice Ranking', userBorda, userSecondCopeland, userSVT)
    makeTable('Randomly Assigned Ranking', randBorda, randSecondCopeland, randSTV)
    #makeTable('One Candidate Always Preferred Ranking', oneHigherBorda, oneHigherSecondCopeland, oneHigherSTV)
    #makeTable('Same Weight and Single Preference Ranking', sameBorda, sameSecondCopeland, sameSTV)





def getUserPref():
    userPref = []
    for x in range(0,len(AGENTS)):
        weight = input("Weight for " + AGENTS[x] + ': ')
        prefArray = []
        for y in range(0, len(CANDIDATES)):
            pref = input("Agent " + AGENTS[x] + ' ranking for ' + CANDIDATES[y] + ': ')
            prefArray.append(pref)
        userPref.append({'agent': AGENTS[x], 'weight': weight, 'prefArray': prefArray})
        print(userPref[len(userPref)-1])
    return userPref

def getRandPref():
    randomPref = []
    for x in range(0, len(AGENTS)):
        randNums = [i for i in range(1, len(CANDIDATES) + 1)]
        shuffle(randNums)
        randWeight = random.randint(1, HIGHESTWEIGHT)
        randomPref.append({'agent': AGENTS[x], 'weight': randWeight, 'prefArray': randNums})
    return randomPref

def getOneHigherPref():
    betterCandidate = int(input('Which candidate index should always be better? (1-' + str(len(CANDIDATES)) + ') ')) - 1
    worseCandidate = int(input('Which candidate index should always be worse? (1-' + str(len(CANDIDATES)) + ') ')) - 1
    oneHigherPref = []
    for x in range(0, len(AGENTS)):
        oneHigherNums = [i for i in range(1, len(CANDIDATES) + 1)]
        shuffle(oneHigherNums)
        if oneHigherNums[betterCandidate] > oneHigherNums[worseCandidate]:
            worsePref = oneHigherNums[betterCandidate]
            betterPref = oneHigherNums[worseCandidate]
            oneHigherNums[betterCandidate] = betterPref
            oneHigherNums[worseCandidate] = worsePref
        oneHigherWeight = random.randint(1, HIGHESTWEIGHT)
        oneHigherPref.append({'agent': AGENTS[x], 'weight': oneHigherWeight, 'prefArray': oneHigherNums})
    return oneHigherPref

def getSameWeightPref():
    sameWeight = random.randint(1, HIGHESTWEIGHT)
    sameCandidate = random.randint(0, len(CANDIDATES) - 1)
    samePref = random.randint(1, len(CANDIDATES))
    sameWeightPref = []
    for x in range(0, len(AGENTS)):
        sameArray = [i for i in range(1, len(CANDIDATES) + 1)]
        sameArray.remove(samePref)
        shuffle(sameArray)
        sameArray.insert(sameCandidate, samePref)
        sameWeightPref.append({'agent': AGENTS[x], 'weight': sameWeight, 'prefArray': sameArray})
    return sameWeightPref

def getMajority(prefArray):
    aBetterB = 0
    numFor = 0
    numAgainst = 0
    majority = []
    a = 0
    b = 1
    n = len(CANDIDATES)  # this is the n of nCr. 2 is the r but it will always be the same
    loopLimit = math.factorial(n) // math.factorial(2) // math.factorial(n - 2)
    for i in range(0, loopLimit):
        for x in range(0, len(AGENTS)):
            prefs = prefArray[x]['prefArray']
            weight = prefArray[x]['weight']
            if (prefs[a] < prefs[b]):
                aBetterB += 1
                numFor += weight
            else:
                numAgainst += weight
        majority.append({'a':CANDIDATES[a], 'b': CANDIDATES[b], 'numFor': numFor, 'numAgainst': numAgainst})
        aBetterB = 0
        numFor = 0
        numAgainst = 0
        b += 1
        if (b == len(CANDIDATES)):
            a += 1
            b = a + 1
    return majority

def getGraph(majority, type):
    digraph = gv.Digraph()
    degreeAndList = [{'type':'Highest', 'degree':0, 'listBeaten': []}, {'type':'High', 'degree':0, 'listBeaten': []},
                     {'type':'Medium', 'degree':0, 'listBeaten': []}, {'type':'Low', 'degree':0, 'listBeaten': []}, {'type': 'Lowest', 'degree':0, 'listBeaten': []}]
    for x in range(0, len(CANDIDATES)):
        digraph.node(CANDIDATES[x])
    for x in range(0, len(majority)):
        item = majority[x]
        if (item['numFor'] > item['numAgainst']):
            digraph.edge(item['a'], item['b'], label=str(item['numFor']) + ', ' + str(item['numAgainst']), weight=str(item['numFor']))
            dict = next((thing for thing in degreeAndList if thing['type'] == item['a']))
            dict['degree'] += 1
            dict['listBeaten'].append(item['b'])
        else:
            digraph.edge(item['b'], item['a'], label=str(item['numAgainst']) + ', ' + str(item['numFor']), weight=str(item['numAgainst']))
            dict = next((thing for thing in degreeAndList if thing['type'] == item['b']))
            dict['degree'] += 1
            dict['listBeaten'].append(item['a'])
    digraph.render('graphImages/' + type + '.gv', view=False)
    return degreeAndList

def bordaOrder(preferences):
    candidateScores = {}
    for y in range(0, len(CANDIDATES)):
        score = 0
        for x in range(0, len(AGENTS)):
            prefArray = preferences[x]['prefArray']
            score += (7 - prefArray[y])
        candidateScores.update({CANDIDATES[y]: score})
    sortedCandidates = sorted(candidateScores, key=candidateScores.get, reverse=True)
    return sortedCandidates

def secondCopelandOrder(preferences):
    candidateScores = {}
    sortedCandidates = sorted(candidateScores, key=candidateScores.get, reverse=True)
    return CANDIDATES#sortedCandidates

def stvOrder(preferences):
    tempCandidates = copy.deepcopy(CANDIDATES)
    prefCopy = copy.deepcopy(preferences)
    sortedCandidates = []
    plurality = calcPlurality(preferences, [])
    lowestPlural = 0
    while(len(tempCandidates) > 0):
        try:
            indexToRemove = plurality.index(lowestPlural)
            plurality[indexToRemove] = -1
            tempCandidates.remove(CANDIDATES[indexToRemove])
            sortedCandidates.insert(0,CANDIDATES[indexToRemove])
            prefCopy = recalcPreferences(prefCopy, tempCandidates)
            plurality = calcPlurality(prefCopy, plurality)
        except:
            lowestPlural += 1

    return sortedCandidates

def recalcPreferences(prefs, candidates):
    for x in range(len(AGENTS)):
        prefArray = prefs[x]['prefArray']
        indexOfHighest = prefArray.index(1)
        try:
            candidates.index(CANDIDATES[indexOfHighest])
        except:
            prefArray[indexOfHighest] = len(CANDIDATES) + 1
            for y in range(len(prefArray)):
                prefArray[y] -= 1
    return prefs


def calcPlurality(preferences, oldPlural):
    plurality = []
    for x in range(len(CANDIDATES)):
        plural = 0
        if(len(oldPlural) == len(CANDIDATES) and oldPlural[x] == -1):
            plurality.append(-1)
            continue
        for y in range(len(AGENTS)):
            prefArray = preferences[y]['prefArray']
            if(prefArray[x] == 1):
                plural += 1
        plurality.append(plural)
    return plurality

def makeTable(votingMethod, borda, secondCopeland, stv):
    numList = []
    for x in range(0, len(CANDIDATES)):
        numList.append(x+1)
    print('\n|| ', votingMethod, ' ||  ', 'Borda','  ||  ', '2nd Copeland', '  ||  ', 'STV', '   ||')
    print('-'*78)
    for x in range(0, len(CANDIDATES)):
        print('||',numList[x],' '*(len(votingMethod)),'||',
              borda[x],' '*(8-len(borda[x])),'||',
              secondCopeland[x],' '*(15-len(secondCopeland[x])),'||',
              stv[x],' '*(7-len(stv[x])),'||')



if __name__ == '__main__':
    main()