from opentest import open_test
import os
import sys
import numpy as np
from ortools.linear_solver import pywraplp

alpha = 1
beta = 0
gamma = 0


def MIPSolution(path):
    b, s, r, m, cap, rs, slots, dist, p, serves, d = open_test(path)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = []
    M = 1
    s = np.array(s, dtype='int64')
    cap = np.array(cap, dtype='int64')
    rs = np.array(rs, dtype='int64')
    slots = np.array(slots, dtype='int64')

    ### creating varirables and adding constraint 1 to the domain fo the variables ###
    for i in range(r):
        x.append([])
        for j in range(b):
            x[i].append([])
            for k in range(s[j]):
                x[i][j].append([])
                for w in range(cap[j]):
                    domain_constraint = 1

                    # constraint 1
                    if not (serves[j][w][rs[i]] == 1
                            and ((slots[rs[i]][j] + k) <= s[j])
                            and dist[i][j] <= d):
                        domain_constraint = 0
                    ### end of constraint 1 ###

                    x[i][j][k].append(solver.IntVar(0, 1 * domain_constraint,
                                                    'x' + str(i) + "-" + str(j) + "-" + str(k) + '-' + str(w)))
    ## constraint 2 ###
    for i in range(r):
        summation = 0
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    summation += x[i][j][k][w]
        solver.Add(summation <= 1)
    ### end of constraint 2 ###

    ### constraint 3 ###
    for i in range(r):
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    for i2 in range(r):
                        if i2 == i or k + slots[rs[i]][j] > s[j]:
                            continue
                        for k2 in range(k, k + slots[rs[i]][j]):
                            solver.Add(x[i][j][k][w] <= (1-x[i2][j][k2][w]))
    # end of constraint 3
    ### objective function ###
    F0 = 0
    F1 = 0
    F2 = 0
    for i in range(r):
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    F0 = F0 + x[i][j][k][w]
                    F1 = F1 + x[i][j][k][w] * dist[i][j]
                    F2 = F2 + x[i][j][k][w] * p[i]

    objective_eqn = (alpha*F0) + (beta*F1) - (gamma*F2)
    solver.Maximize(objective_eqn)
    solver.SetTimeLimit(5000)
    solver.Solve()
    score = solver.Objective().Value()
    solution = []
    for i in range(r):
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    if x[i][j][k][w].solution_value() == 1:
                        solution.append((i+1, j+1, k+1, w+1))

    return score, solution


if __name__ == '__main__':
    folderName = sys.argv[1]
    try:
        os.mkdir(folderName+"_output")
    except FileExistsError:
        nothing = ''
    try:
        os.mkdir(folderName+"_output/MIP")
    except FileExistsError:
        nothing = ''
    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        try:
            matches, solution = MIPSolution(path)
        except:
            matches = 0
            solution = []
        output = open(folderName+"_output/MIP/" +
                      filename[:len(filename)-3]+".out", "w")
        output.write(str(matches)+"\n")
        for i in range(len(solution)):
            if(solution[i] != -1):
                (i, takenBranch, startSlot, counter) = solution[i]
                output.write(str(i) + " " + str(takenBranch) +
                             " " + str(startSlot) + " " + str(counter) + "\n")
        print(filename+' Done')


def solve(path):

    try:
        matches, solution = MIPSolution(path)
    except:
        matches = "0"
        solution = []
    
    output= str(matches)+"\n"
    for i in range(len(solution)):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter) = solution[i]
            output += str(i) + " " + str(takenBranch) +" " + str(startSlot) + " " + str(counter) + "\n"
    return output