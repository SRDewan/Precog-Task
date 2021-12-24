import numpy as np
import random
import copy

def getData():
    adj = np.zeros((11000, 11000))
    prof = {}

    with open('tinyProfiles.txt') as f:
        lines = f.readlines()
        for line in lines:
            split = line.split('\t')
            prof[split[0]] = np.array(split[1:])

    with open('smallGraph.txt') as f:
        lines = f.readlines()
        for line in lines:
            split = line.split()
            if split[0] in prof.keys() and split[1] in prof.keys():
                v1 = int(split[0])
                v2 = int(split[1])
                adj[v1][v2] = 1
                adj[v2][v1] = 1

    return adj, prof

def globalA(adj, prof):
    pass

def evaluate(A, userIds, seed):
    recall = (len(set(A) & set(userIds)) - len(seed)) / (len(userIds) - len(seed))
    precision = (len(set(A) & set(userIds)) - len(seed)) / (len(A) - len(seed))
    print("Recall = {}, Precision = {}".format(recall, precision))

def getModularity(adj, comms):
    Q = 0
    tot = np.sum(adj)

    for ind in range(len(comms)):
        comm = comms[ind]
        eii = 0
        ai = 0

        for i in range(len(comm)):
            row = np.array(adj[comm[i], :])
            eii += np.sum(row[comm])
            ai += np.sum(row)

        Q += (eii / tot - (ai / tot) ** 2)

    return Q

def getConductance(adj, A):
    eaa = 0
    eab = 0
    for i in range(len(A)):
        row = np.array(adj[A[i], :])
        eaa += np.sum(row[A])
        eab += (np.sum(row) - np.sum(row[A]))

    ebb = np.sum(adj) - eaa - eab
    ea = eaa + eab
    eb = ebb + eab
    c = (eaa / (eaa + eab)) - (ea * ea / (ea * ea + ea * eb))
    return c

def local(adj, prof, ind, val):
    profArr = np.array(list(prof.values()), dtype=object)
    userInds = np.where(profArr[:, ind] == val)[0]
    userIds = np.array(list(prof.keys()))[userInds].astype(int)
    allUsers = np.array(list(prof.keys()), dtype=object).astype(int)

    for percent in np.arange(0.1, 1.1, 0.1):
        size = int(len(userIds) * percent)
        print(percent, size)
        A = random.sample(list(userIds), size)
        curr = getConductance(adj, A)
        seed = copy.deepcopy(A)

        while True:
            maxi = curr
            addV = -1
            print(len(A))

            for v in range(len(profArr)):
                if allUsers[v] in A:
                    continue

                newA = copy.deepcopy(A)
                newA.append(allUsers[v])
                metric = getConductance(adj, newA)

                if metric > maxi:
                    maxi = metric
                    addV = allUsers[v]

            if addV == -1:
                break

            A.append(addV)
            curr = maxi

        evaluate(A, userIds, seed)

def main():
    adj, prof = getData()
    local(adj, prof, 3, 'zilinsky kraj, zilina')
    # globalA(adj, prof)

if __name__ == "__main__":
    main()
