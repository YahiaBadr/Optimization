import sys
import opentest

def baselineSolution(testnum):
    
    def sortPair(e):
        return e['priority']

        
    def isSlotAvailable(branch, service):
        slotsNeeded = int(slots[service][branch])
        for i in range(int(s[branch])):
            if( i + slotsNeeded >= s[branch]):
                break
            intersection = branchSolts[branch][i]
            for j in range(slotsNeeded):
                intersection = list(set(intersection) & set(branchSolts[branch][i + j]))
            if(len(intersection) > 0):
                for counter in intersection:
                    if(serves[branch][counter - 1][service] == 1):
                        return True
        return False


    def takeSlot(branch, service):
        slotsNeeded = int(slots[service][branch])
        for i in range(int(s[branch])):
            if( i + slotsNeeded >= s[branch]):
                break
            intersection = branchSolts[branch][i]
            for j in range(slotsNeeded):
                intersection = list(set(intersection) & set(branchSolts[branch][i + j]))
            if(len(intersection) > 0):
                for counter in intersection:
                    if(serves[branch][counter - 1][service] == 1):
                        for j in range(slotsNeeded):
                            branchSolts[branch][i + j].pop(branchSolts[branch][i + j].index(counter))
                        return i, counter

    b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(testnum)
    branchSolts = []
    for i in range(b):
        branchSolts.append([])
        for j in range(int(s[i])):
            branchSolts[i].append([])
            for k in range(int(cap[i])):
                branchSolts[i][j].append(k+1)

    sorted_requests = []
    for i in range(r):
        sorted_requests.append({'service': int(rs[i]), 'priority': p[i]})

    sorted_requests.sort(key=sortPair)

    solution = [-1] * r
    matches = 0
    for i in range(r):
        service = sorted_requests[i]['service']
        minDist = sys.maxsize
        takenBranch = -1
        for branch in range(b):
            if(minDist > dist[i][branch] and dist[i][branch] <= d and isSlotAvailable(branch, service)):
                takenBranch = branch
        if(takenBranch != -1):
            startSlot, counter = takeSlot(takenBranch, service)
            solution[i] = ((i+1, takenBranch, startSlot, counter))
            matches += 1
    
    print(matches)
    for i in range(r):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter) = solution[i]
            print(i, takenBranch, startSlot, counter)

    return solution


baselineSolution(0)
