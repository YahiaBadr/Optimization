
import sys
import os

from numpy import random
import opentest
import numpy as np
from numpy.random import randint
from numpy.random import rand

b = 0
s = 0
r = 0
m = 0
n = 0
rs = []
cap = []
slots = []
dist = []
p = []
serves = []
d = 0
ids = []
unmap = []
cand = []

# Total iterations
n_iter = 100
# bits
# population size
n_pop = 100
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 0

alpha = 1
beta = 0
gamma = 0


# objective function
def objective(chromosome):
    z = 0
    for i in range(r):
        if chromosome[i] != -1:
            z += 1
    return z

# tournament based selection


def selection(pop, scores, k=3):
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# crossover two parents to create two children


def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross and len(p1) > 2:
        # select crossover point
        pt = randint(1, len(p1)-2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    # for i in range(r):
    #     if p1[i] in cand[i] and p2[i] in cand[i] and (c1[i] not in cand[i] or c2[i] not in cand[i]):
    #         print('problemo')

    return [c1, c2]


# mutation operator


def mutation(chromosome, r_mut):
    taken = [False] * n
    genes = []
    for i in range(r):
        # check for a mutation
        if rand() < r_mut:
            genes.append(i)
            chromosome[i] = -1
        else:
            if chromosome[i] != -1:
                j, w, k = unmap[chromosome[i]]
                for k2 in range(k, k+slots[rs[i]][j]):
                    # print(i, chromosome[i], cand[i])
                    taken[ids[j][w][k2]] = True

    for i in genes:
        choice = random.randint(0, len(cand[i])+1)
        if choice == len(cand[i]):
            continue
        if not is_valid_gene(taken, i, cand[i][choice]):
            continue
        j, w, k = unmap[cand[i][choice]]
        for k2 in range(k, k+slots[rs[i]][j]):
            taken[ids[j][w][k2]] = True
        chromosome[i] = choice


def is_valid_gene(taken, i, idx):
    j, w, k = unmap[idx]
    for k2 in range(k, k+slots[rs[i]][j]):
        if taken[ids[j][w][k2]]:
            return False
    return True


def generate_random_chromosome():
    taken = [False]*n
    chromosome = [-1]*r
    for i in range(r):
        choice = random.randint(0, len(cand[i])+1)
        if choice == len(cand[i]):
            continue
        if not is_valid_gene(taken, i, cand[i][choice]):
            continue
        j, w, k = unmap[cand[i][choice]]
        for k2 in range(k, k+slots[rs[i]][j]):
            taken[ids[j][w][k2]] = True
        chromosome[i] = cand[i][choice]

    return chromosome


def genetic_algorithm():
    # initial population of random solutions
    pop = [generate_random_chromosome() for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = pop[0], objective(pop[0])
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [objective(c) for c in pop]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))

        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    # print(best)
    return (best_eval, best)


def HeuristicSolution(testnum):
    global memo, cand, n, b, s, r, m, cap, rs, slots, dist, p, serves, d, ids, unmap, r_mut

    b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(
        testnum)

    s = np.array(s, dtype='int64')
    cap = np.array(cap, dtype='int64')
    rs = np.array(rs, dtype='int64')
    slots = np.array(slots, dtype='int64')

    ids = []
    unmap = []
    n = 0
    cand = [None]*r

    for i in range(b):
        ids.append([])
        for j in range(cap[i]):
            ids[i].append([])
            for k in range(s[i]):
                ids[i][j].append(n)
                unmap.append((i, j, k))
                n = n+1

    for i in range(r):
        cand[i] = []
    for j in range(b):
        for w in range(cap[j]):
            for k in range(s[j]):
                if serves[j][w][rs[i]] and dist[i][j] <= d and k+slots[rs[i]][j] <= s[j]:
                    cand[i].append(ids[j][w][k])

    r_mut = 1.0 / float(min(20, n))
    score, chromosome = genetic_algorithm()
    solution = []
    for i in range(r):
        if chromosome[i] != -1:
            j, w, k = unmap[chromosome[i]]
            solution.append((i+1, j+1, k+1, w+1))
    return score, solution


if __name__ == '__main__':
    folderName = sys.argv[1]

    try:
        os.mkdir(folderName+"_output")
    except FileExistsError:
        nothing = ''
    try:
        os.mkdir(folderName+"_output/Heuristic")
    except FileExistsError:
        nothing = ''
    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        matches, solution = HeuristicSolution(path)
        output = open(folderName+"_output/Heuristic/" +
                      filename[:len(filename)-3]+".out", "w")
        output.write(str(matches)+"\n")
        for i in range(len(solution)):
            if(solution[i] != -1):
                (i, takenBranch, startSlot, counter) = solution[i]
                output.write(str(i) + " " + str(takenBranch) + " " +
                             str(startSlot) + " " + str(counter) + "\n")
        print(filename+' Done')
