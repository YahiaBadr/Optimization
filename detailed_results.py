import sys
import os
import pandas as pd
import numpy as np
import opentest


def get_matches(path):
    matches = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for i in range(1, len(lines)):
            line = lines[i].strip().split(' ')
            matches.append(
                (int(line[0])-1, int(line[1])-1, int(line[2])-1, int(line[3])-1))
    return matches


def calculate_distance(matches, r, n, dist, p, slots):
    ans = 0
    for (i, j, _, _) in matches:
        ans += dist[i][j]
    return ans


def calculate_priority(matches, r, n, dist, p, slots):
    ans = 0
    for (i, _, _, _) in matches:
        ans += p[i]
    return ans


def calculate_requests_fullfillment(matches, r, n, dist, p, slots):
    return len(matches)/r*100


def calculate_branch_utilization(macthes, r, n, dist, p, slots):
    ans = 0
    for (i, j, _, _) in macthes:
        ans += slots[rs[i]][j]
    ans = (ans/n)*100
    return ans


if __name__ == '__main__':
    folderName = sys.argv[1]
    dir_path = folderName+'_output/deatiled_results'
    os.makedirs(dir_path, exist_ok=True)

    metrics = ['Branch Utilization', 'Request Satisfaction',
               'Total Distance', 'Total Priority']

    solvers = ['MIP', 'DP', 'Baseline', 'Heuristic']

    methods = [calculate_branch_utilization, calculate_requests_fullfillment,
               calculate_distance, calculate_priority]

    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        summary_df = pd.DataFrame(
            columns=['metric', 'MIP', 'DP', 'Baseline', 'Heuristic'])
        summary_dir = os.path.join(dir_path, 'test%i.csv' % testnum)

        b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(
            path)
        s = np.array(s, dtype='int64')
        cap = np.array(cap, dtype='int64')
        rs = np.array(rs, dtype='int64')
        slots = np.array(slots, dtype='int64')

        matches = []
        for j in range(4):
            filepath = folderName+'_output/' + \
                solvers[j]+'/'+filename.replace('in', 'out')
            matches.append(get_matches(filepath))

        n = 0
        for i in range(b):
            n += s[i]*cap[i]

        for i in range(4):
            res = []
            for j in range(4):
                res.append(methods[i](matches[j], r, n, dist, p, slots))

            new_row = {
                'metric': metrics[i],
                'MIP': res[0],
                'DP': res[1],
                'Baseline': res[2],
                'Heuristic': res[3],
            }

            summary_df = summary_df.append(new_row, ignore_index=True)
        summary_df.to_csv(summary_dir, index=False)
        print(filename+' Done')
