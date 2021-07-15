import os
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
        sorted_requests.append({'indx': i, 'service': int(rs[i]), 'priority': p[i]})

    sorted_requests.sort(key=sortPair)

    solution = [-1] * r
    matches = 0
    for i in range(r):
        service = sorted_requests[i]['service']
        indx = sorted_requests[i]['indx']
        minDist = sys.maxsize
        takenBranch = -1
        for branch in range(b):
            if(minDist > dist[indx][branch] and dist[indx][branch] <= d and isSlotAvailable(branch, service)):
                takenBranch = branch
        if(takenBranch != -1):
            startSlot, counter = takeSlot(takenBranch, service)
            solution[indx] = ((indx + 1, takenBranch + 1, startSlot + 1, counter, service))
            matches += 1

    return matches, solution




if __name__=='__main__':
    folderName = sys.argv[1]
    try:
        os.mkdir(folderName+"_output")
    except FileExistsError:
        nothing = ''
    try:
        os.mkdir(folderName+"_output/Baseline")
    except FileExistsError:
        nothing = ''
    for filename in sorted(os.listdir("./"+folderName), key = lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        matches, solution = baselineSolution(path)
        output = open(folderName+"_output/Baseline/"+filename[:len(filename)-3]+".out", "w")
        output.write(str(matches)+"\n")
        for i in range(len(solution)):
            if(solution[i] != -1):
                (i, takenBranch, startSlot, counter, service) = solution[i]
                output.write(str(i) + " " + str(takenBranch) + " " + str(startSlot) + " " + str(counter) + "\n")
        print(filename+' Done')




def solve(path):
    matches, solution = baselineSolution(path)
    output = (str(matches)+"\n")
    for i in range(len(solution)):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter, service) = solution[i]
            output+=(str(i) + " " + str(takenBranch) + " " + str(startSlot) + " " + str(counter) + "\n")
    return output