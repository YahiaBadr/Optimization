from opentest import open_test
import os
import sys
import numpy as np
from ortools.linear_solver import pywraplp

alpha = 1
beta = 0
theta = 0


def MIPSolution(path):
    b, s, r, m, cap, rs, slots, dist, p, serves, d = open_test(path)
    s = np.array(s, dtype='int64')
    cap = np.array(cap, dtype='int64')
    rs = np.array(rs, dtype='int64')
    slots = np.array(slots, dtype='int64')

    # Lowering default primal tolerance
    # refer to this for more details: https://github.com/google/or-tools/discussions/2295
    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(
        pywraplp.MPSolverParameters.PRIMAL_TOLERANCE, 0.001)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    objective = solver.Objective()
    vars = []

    for i in range(r):
        vars.append([])
        sum = 0
        for j in range(b):
            vars[i].append([])
            for k in range(s[j]):
                vars[i][j].append([])
                for w in range(cap[j]):
                    x = None
                    if serves[j][w][rs[i]] and dist[i][j] <= d and (slots[rs[i]][j] + k) <= s[j]:
                        x = solver.IntVar(0, 1, 'x%i%i%i%i' % (i, j, k, w))
                        sum += x
                        objective.SetCoefficient(
                            x, (alpha-beta*dist[i][j]+p[i]*theta))
                    vars[i][j][k].append(x)
        solver.Add(sum <= 1)

    for i in range(r):
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    if vars[i][j][k][w] is None:
                        continue
                    for k2 in range(k, k+slots[rs[i]][j]):
                        for i2 in range(r):
                            if i == i2 or vars[i2][j][k2][w] is None:
                                continue
                            solver.Add(vars[i][j][k][w] <=
                                       (1-vars[i2][j][k2][w]))

    objective.SetMaximization()
    solver.SetTimeLimit(10000)
    status = solver.Solve(solver_parameters)
    score = objective.Value()
    solution = []
    for i in range(r):
        for j in range(b):
            for k in range(s[j]):
                for w in range(cap[j]):
                    if vars[i][j][k][w] is None:
                        continue
                    if vars[i][j][k][w].solution_value() == 1:
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

    output = str(matches)+"\n"
    for i in range(len(solution)):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter) = solution[i]
            output += str(i) + " " + str(takenBranch) + " " + \
                str(startSlot) + " " + str(counter) + "\n"
    return output
