import numpy as np
from ortools.linear_solver import pywraplp

alpha = 1
beta = 1
gamma = 1


def open_test(testnum):

    path = "./testset_" + str(1) + "/test_" + str(testnum) + ".in"

    f = open(path, "r")
    line = f.readline().split(" ")
    b = int(line[0])
    r = int(line[1])
    m = int(line[2])
    d = int(line[3])
    slots = np.zeros([m, b])

    for z in range(m):
        line = f.readline().split(" ")
        for j in range(b):
            slots[z][j] = int(line[j])

    r_locations = np.zeros([r, 2])
    rs = np.zeros(r)
    p = np.zeros(r)

    for i in range(r):
        line = f.readline().split(" ")
        xi = int(line[0])
        yi = int(line[1])
        pi = int(line[2])
        rsi = int(line[3])
        r_locations[i] = [xi, yi]
        p[i] = pi
        rs[i] = rsi

    b_locations = np.zeros([b, 2])
    s = np.zeros(b)
    cap = np.zeros(b)
    serves = []

    for i in range(b):
        line = f.readline().split(" ")
        xi = int(line[0])
        yi = int(line[1])
        si = int(line[2])
        capi = int(line[3])
        b_locations[i] = [xi, yi]
        s[i] = si
        cap[i] = capi
        serves.append([])
        for j in range(capi):
            line = f.readline().split(" ")
            n = int(line[0])
            set_of_served = set()
            serves[i].append([])
            for k in range(n):
                set_of_served.add(int(line[k+1]))
            for z in range(m):
                if z in set_of_served:
                    serves[i][j].append(1)
                else:
                    serves[i][j].append(0)

    dist = distances(r_locations, b_locations)
    return b, s, r, m, cap, rs, slots, dist, p, serves, d


def distances(r_positions, b_positions):
    r = len(r_positions)
    b = len(b_positions)
    dist = np.zeros([r, b])
    for i in range(r):
        for j in range(b):
            dist[i][j] = np.linalg.norm(r_positions[i] - b_positions[j])
    return dist

def MIP_solver(b, s, r, m, cap, rs, slots, dist, p, serves, d):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = []
    M = solver.infinity()
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

                    #constraint 1
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
                        if i2 == i:
                            continue
                        for k2 in range(k, k + slots[rs[i]][j]-3):
                            solver.Add(x[i][j][k][w] <= M * (1-x[i2][j][k2][w]))
    ### end of constraint 3


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
    solver.Solve()
    Z = solver.Objective().Value()
    sol = []
    matchings = 0
    for i in range(len(x)):
        sol.append([])
        for j in range(len(x[i])):
            sol[i].append([])
            for k in range(len(x[i][j])):
                sol[i][j].append([])
                for w in range(len(x[i][j][k])):
                    sol[i][j][k].append(x[i][j][k][w].solution_value())
                    matchings += x[i][j][k][w].solution_value()

    return Z, sol, matchings/r
