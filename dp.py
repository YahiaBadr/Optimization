import os
import sys
import opentest
import numpy as np

memo = []
b = 0
s = 0
r = 0
m = 0
rs = []
cap = []
slots = []
dist = []
p = []
serves = []
d = 0
ids = []
cand = []

alpha = 1
beta = 0
gamma = 0

def dp(i, mask):
    if i == r:
        return 0

    if memo[i][mask] != -1:
        return memo[i][mask]

    best = dp(i+1, mask)
    for (j, w) in cand[i]:
        for k in range(s[j]):
            check = checkValidPlacement(i, mask, j, k, w)
            if check != -1:
                best = max(best, alpha - beta *
                           dist[i][j] + gamma*p[i]+dp(i+1, mask | check))
    memo[i][mask] = best
    return best


def checkValidPlacement(i, mask, j, k, w):
    if k+slots[rs[i]][j] > s[j]:
        return -1

    occ = 0
    for k2 in range(k, k+slots[rs[i]][j]):
        if (mask & (1 << ids[j][k2][w]) != 0):
            return -1
        occ |= (1 << ids[j][k2][w])

    return occ


def trace(i, mask):
    if i == r:
        return []

    best = dp(i, mask)
    if best == dp(i+1, mask):
        return trace(i+1, mask)

    for (j, w) in cand[i]:
        for k in range(s[j]):
            check = checkValidPlacement(i, mask, j, k, w)
            if check != -1 and 1+dp(i+1, mask | check) == best:
                res = trace(i+1, mask | check)
                return [(i+1, j+1, k+1, w+1)]+res


def dpSolution(testnum):
    global memo, cand, b, s, r, m, cap, rs, slots, dist, p, serves, d, ids
    b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(
        testnum)
    ids = []
    cnt = 0
    s = np.array(s, dtype='int64')
    cap = np.array(cap, dtype='int64')
    rs = np.array(rs, dtype='int64')
    slots = np.array(slots, dtype='int64')

    cand = [None]*r
    for i in range(b):
        ids.append([])
        for j in range(s[i]):
            ids[i].append([])
            for _ in range(cap[i]):
                ids[i][j].append(cnt)
                cnt = cnt+1

    for i in range(r):
        cand[i] = []
        for j in range(b):
            for w in range(cap[j]):
                if serves[j][w][rs[i]] and dist[i][j] <= d:
                    cand[i].append((j, w))

    memo = [[-1]*(1 << cnt) for _ in range(r)]

    return dp(0, 0)


if __name__ == '__main__':
    folderName = sys.argv[1]

    try:
        os.mkdir(folderName+"_output")
    except FileExistsError:
        nothing = ''
    try:
        os.mkdir(folderName+"_output/DP")
    except FileExistsError:
        nothing = ''
    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        matches = dpSolution(path)
        solution = trace(0, 0)
        output = open(folderName+"_output/DP/" +
                      filename[:len(filename)-3]+".out", "w")
        output.write(str(matches)+"\n")
        for i in range(len(solution)):
            if(solution[i] != -1):
                (i, takenBranch, startSlot, counter) = solution[i]
                output.write(str(i) + " " + str(takenBranch) + " " +
                             str(startSlot) + " " + str(counter) + "\n")


def solve(path):
    matches = dpSolution(path)
    solution = trace(0, 0)
    output = (str(matches)+"\n")
    for i in range(len(solution)):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter) = solution[i]
            output += (str(i) + " " + str(takenBranch) + " " +
                       str(startSlot) + " " + str(counter) + "\n")
    return output
