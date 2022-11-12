import random
import math


def readdoc():
    matrice = []
    try:
        # with open('test.txt', 'r') as f:
        #     matrice = [[int(num) for num in line.split(' ')] for line in f]

        with open("test.txt ") as textFile:
            for line in textFile:
                number = [item.strip() for item in line.split(' ')]
                matrice.append([x for x in number if x.isdigit()])
    except FileExistsError:
        print("that file does not exist")

    for n, i in enumerate(matrice):
        for k, j in enumerate(i):
            matrice[n][k] = int(j)
    return matrice


def leavesTime(vector, matrice):
    # list of the end of each machine
    end = [0] * matrice[0][1]
    # matrice of the result
    result = [[0 for x in range(matrice[0][1])] for y in range(matrice[0][0])]

    # retreive the placement of the time in the matrice
    placement = []
    x = 1
    for machine in range(matrice[0][1]):
        if machine == 0:
            placement.append(1)
        else:
            x = x + 2
            placement.append(x)

    # loop the  vector and put the end time the start
    for job in vector:
        # start loop
        for machine in range(matrice[0][1]):
            if machine == 0:
                end[0] = end[0] + matrice[job][1]
            else:
                if end[machine] < end[machine - 1]:
                    end[machine] = end[machine - 1] + matrice[job][placement[machine]]
                else:
                    end[machine] = end[machine] + matrice[job][placement[machine]]

            result[job - 1][machine] = end[machine]
        # end loop

    return max(max(result))


def randomsearch(matrice):
    for i in range(5):
        li = range(1, matrice[0][0] + 1)
        vector = random.sample(li, 5)

        if i == 0:
            result = leavesTime(vector, matrice)
            best_vector = vector
        else:
            if leavesTime(vector, matrice) < result:
                result = leavesTime(vector, matrice)
                best_vector = vector
            else:
                continue

    return result, best_vector


def localsearch(verctor, matrice):
    best_vector = verctor
    best_result = leavesTime(verctor, matrice)

    x = True
    while x:
        for i in range(len(verctor)):
            for j in range(i + 1, len(verctor)):
                permutation = verctor[i]
                verctor[i] = verctor[j]
                verctor[j] = permutation

                if leavesTime(verctor, matrice) < best_result:
                    best_result = leavesTime(verctor, matrice)
                    best_vector = verctor[:]

                permutation = verctor[i]
                verctor[i] = verctor[j]
                verctor[j] = permutation

        if best_vector != verctor:
            x = False

    return best_vector


def pseudocode(alpha, L, Tf, vercot, matrice):
    sact = vercot
    t = leavesTime(sact, matrice) * 0.3

    while t > Tf:
        for i in range(L):
            # generate random neighbor
            # generate 2 random placement in the vector
            x = random.randint(0, len(vercot) - 1)
            y = random.randint(0, len(vercot) - 1)
            # do the permutation and save the new neighbor in the scant
            scant = vercot[:]
            permutation = scant[x]
            scant[x] = scant[y]
            scant[y] = permutation
            # calculate delta
            delta = leavesTime(scant, matrice) - leavesTime(sact, matrice)
            # the condition
            # the random.random() generate a random number between 0 and 1
            if random.random() < math.exp(-delta / t) or delta < 0:
                sact = scant

            t = t - alpha

    sact = localsearch(sact, matrice)

    return sact, leavesTime(sact, matrice)


def genetico(matrice,generations):
    # create random 101 results
    vectors = []
    for i in range(101):
        result, vector = randomsearch(matrice)
        vectors.append([vector, result])

    for generation in range(generations):
        # creating the best 100
        bests = []
        for i in range(100):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            if vectors[x][1] < vectors[y][1]:
                bests.append(vectors[x])
            else:
                bests.append(vectors[y])

        # creating childrens
        childrens = []
        # get the 40%
        for i in range(40):
            childrens.append(vectors[i])
        # get the other 60%
        for i in range(40, 99, 2):
            # get the middle crosses
            parent1 = bests[i][0]
            parent2 = bests[i + 1][0]
            firstCrossPoint = random.randint(1, len(parent1) - 2)
            secondCrossPoint = random.randint(firstCrossPoint + 1, len(parent1) - 1)
            parent1MiddleCross = parent1[firstCrossPoint:secondCrossPoint]
            parent2MiddleCross = parent2[firstCrossPoint:secondCrossPoint]
            # create the childrens
            child1 = []
            child2 = []
            # create child 1
            for j in range(0, firstCrossPoint):
                if parent1[j] in parent2MiddleCross:
                    child1.append(parent2[j])
                else:
                    child1.append(parent1[j])
            child1 = (child1 + parent2MiddleCross)
            for j in range(secondCrossPoint, len(parent1)):
                if parent1[j] in child1:
                    child1.append(parent2[j])
                else:
                    child1.append(parent1[j])
            # create child 2
            for j in range(0, firstCrossPoint):
                if parent2[j] in parent1MiddleCross:
                    child2.append(parent1[j])
                else:
                    child2.append(parent2[j])
            child2 = (child2 + parent1MiddleCross)
            for j in range(secondCrossPoint, len(parent2)):
                if parent2[j] in child2:
                    child2.append(parent1[j])
                else:
                    child2.append(parent2[j])

            # add the childrens to our list
            childrens.append([child1, leavesTime(child1, matrice)])
            childrens.append([child2, leavesTime(child2, matrice)])

        # permutation
        for i in range(5):
            firstCrossPoint = random.randint(1, len(childrens[i][0]) - 2)
            secondCrossPoint = random.randint(firstCrossPoint + 1, len(childrens[i][0]) - 1)
            j = childrens[i][0]
            permutaiton = j[firstCrossPoint]
            j[firstCrossPoint] = j[secondCrossPoint]
            j[secondCrossPoint] = permutaiton

        # adding the elite solution
        best = vectors[0][1]
        index = 0
        for i in range(100):
            if vectors[i][1] < best:
                best = vectors[i][1]
                index = i
            else:
                continue
        childrens.append(vectors[index])

    best=childrens[0][1]
    index=0
    for i in range(100):
        if childrens[i][1] < best:
            best = vectors[i][1]
            index = i
        else:
            continue
    return childrens[i][0],childrens[i][1]



def main():
    # print(leavesTime([4, 2, 5, 1, 3], readdoc()))
    # print(randomsearch(readdoc()))
    # print(localsearch([6,3,11,7,8,5,1,2,4,9,10],readdoc()))

    # generate a rendom vector
    # result,random_vector = randomsearch(readdoc())
    # print(pseudocode(1, 1000, 0.0001, random_vector, readdoc()))
    print(genetico(readdoc(),10))


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
