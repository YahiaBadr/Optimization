import sys
import os
import pandas as pd
import numpy as np
import opentest


if __name__ == '__main__':
    folderName = sys.argv[1]
    dir_path = folderName+'_output/deatiled_results'
    os.makedirs(dir_path, exist_ok=True)

    metrics = ['Branch Utilization', 'Request Satisfaction',
               'Total Distance', 'Total Priority']
    
    

    for filename in sorted(os.listdir("./"+folderName), key=lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        summary_df = pd.DataFrame(
            columns=['metric', 'MIP', 'DP', 'Baseline', 'Heuristic'])
        summary_dir = os.path.join(dir_path, 'test%i.csv' % testnum)

        b, s, r, m, cap, rs, slots, dist, p, serves, d = opentest.open_test(
            testnum)
        s = np.array(s, dtype='int64')
        cap = np.array(cap, dtype='int64')
        rs = np.array(rs, dtype='int64')
        slots = np.array(slots, dtype='int64')

        n = 0
        for i in range(b):
            n += s[i]*cap[i]

        with open(path, 'r') as f:
            line = f.readline().split(" ")
            b = int(line[0])
            r = int(line[1])
            d = int(line[3])

        print(filename+' Done')

        # new_row = {
        #     'test_case': testnum,
        #     'r': r,
        #     'b': b,
        #     'd': d,
        #     'dp_z': dp_z,
        #     'dp_t': dp_t,
        #     'mip_z': mip_z,
        #     'mip_t': mip_t,
        #     'baseline_z': baseline_z,
        #     'baseline_t': baseline_t,
        #     'heuristics_z': heuristics_z,
        #     'heuristics_t': heuristics_t
        # }
        # summary_df = summary_df.append(new_row, ignore_index=True)
        # summary_df.to_csv(summary_dir, index=False)
