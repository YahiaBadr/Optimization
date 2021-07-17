
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

# Number of generations
n_gen = 100
# population size
pop_size = 250
# crossover rate
r_cross = 0.9
# mutation rate (Default Value, will be changed according to input)
r_mut = 0.1

alpha = 1
beta = 0
gamma = 0


def objective(chromosome):
    ''' Calculates the fitness value of a chromosome'''
    z = 0
    for i in range(r):
        if chromosome[i] != -1:
            j = unmap[chromosome[i]][0]
            z += alpha + beta*dist[i][j] + gamma*p[i]
    return z


def selection(pop, scores, k=5):
    ''' Perform Torunament Based Selection'''
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def check_miscarriage(genome):
    ''' Checks if the genome resulting from the crossover has any clashes'''
    taken = [False]*n
    for i in range(r):
        j, w, k = unmap[genome[i]]
        for k2 in range(k, k+slots[rs[i]][j]):
            if taken[ids[j][w][k2]]:
                return True
            taken[ids[j][w][k2]] = True
    return False


def crossover(p1, p2, r_cross):
    ''' Perform Cross over of two parents to create two children'''
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross and len(p1) > 3:
        # select crossover point
        pt = randint(1, len(p1)-2)
        # perform crossover
        cand1 = p1[:pt] + p2[pt:]
        cand2 = p2[:pt] + p1[pt:]
        # check for miscarriage
        if not check_miscarriage(cand1):
            c1 = cand1
        if not check_miscarriage(cand2):
            c2 = cand2
    return [c1, c2]


def mutation(chromosome, r_mut):
    ''' Performs Mutation Operation'''
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
        chromosome[i] = cand[i][choice]


def is_valid_gene(taken, i, idx):
    ''' Checks if possible to assign value idx to gene i'''
    j, w, k = unmap[idx]
    for k2 in range(k, k+slots[rs[i]][j]):
        if taken[ids[j][w][k2]]:
            return False
    return True


def generate_random_chromosome():
    ''' Generates random chromosome with valid genes'''
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
    # initial population
    pop = [generate_random_chromosome() for _ in range(pop_size)]

    best, best_eval = pop[0], objective(pop[0])
    # enumerate generations
    for gen in range(n_gen):
        # evaluate all candidates in the population
        scores = [objective(c) for c in pop]

        for i in range(pop_size):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]

        # select parents
        selected = [selection(pop, scores) for _ in range(pop_size)]
        # create the next generation
        children = list()
        for i in range(0, pop_size, 2):
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
                    if serves[j][w][rs[i]] == 1 and slots[rs[i]][j] + k <= s[j] and dist[i][j] <= d:
                        cand[i].append(ids[j][w][k])
    r_mut = 1.0 / float(min(10, n))
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


def solve(path):
    matches, solution = HeuristicSolution(path)
    output = str(matches)+"\n"
    for i in range(len(solution)):
        if(solution[i] != -1):
            (i, takenBranch, startSlot, counter) = solution[i]
            output += (str(i) + " " + str(takenBranch) + " " +
                       str(startSlot) + " " + str(counter) + "\n")
    return output
