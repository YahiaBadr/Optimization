import dp
import mip
import heuristics
import baseline
import sys
import os
import pandas as pd
import time


def solve_baseline(path, folderName, filename):

    start_time = time.time()
    matches, _ = baseline.baselineSolution(path)
    duration_time = time.time() - start_time
    return matches, duration_time


def solve_heuristics(path, folderName, filename):
    start_time = time.time()
    matches, _ = heuristics.HeuristicSolution(path)
    duration_time = time.time() - start_time
    return matches, duration_time


def solve_dp(path, folderName, filename):

    start_time = time.time()
    matches = dp.dpSolution(path)
    duration_time = time.time() - start_time
    return matches, duration_time


def solve_mip(path, folderName, filename):
    start_time = time.time()
    try:
        matches, _ = mip.MIPSolution(path)
    except:
        matches = 0
    duration_time = time.time() - start_time
    return matches, duration_time


if __name__ == '__main__':
    folderName = sys.argv[1]
    dir_path = folderName+'_output'
    os.makedirs(dir_path, exist_ok=True)
    summary_df = pd.DataFrame(columns=['test_case', 'r', 'b', 'd', 'mip_z',
                                       'mip_t',  'dp_z', 'dp_t', 'baseline_z', 'baseline_t', 'heuristics_z', 'heuristics_t'])
    summary_dir = os.path.join(dir_path, 'summary.csv')

    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename

        dp_z, dp_t = solve_dp(path, folderName, filename)
        mip_z, mip_t = solve_mip(path, folderName, filename)
        baseline_z, baseline_t = solve_baseline(path, folderName, filename)
        heuristics_z, heuristics_t = solve_heuristics(
            path, folderName, filename)
        with open(path, 'r') as f:
            line = f.readline().split(" ")
            b = int(line[0])
            r = int(line[1])
            d = int(line[3])

        print(filename+' Done')

        new_row = {
            'test_case': testnum,
            'r': r,
            'b': b,
            'd': d,
            'dp_z': dp_z,
            'dp_t': dp_t,
            'mip_z': mip_z,
            'mip_t': mip_t,
            'baseline_z': baseline_z,
            'baseline_t': baseline_t,
            'heuristics_z': heuristics_z,
            'heuristics_t': heuristics_t
        }
        summary_df = summary_df.append(new_row, ignore_index=True)
    summary_df.to_csv(summary_dir, index=False)
