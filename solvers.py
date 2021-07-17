



import os 
import dp ,baseline,mip,heuristics
from create_map import draw_map
import numpy as np

def solve(solver,goals_u): 
    dir_path = 'web_IO'
    os.makedirs(dir_path,exist_ok=True)
    goals = goals_u.split("#")
    output = []
    if solver == 'dp':
        
        for goal in goals :
            path = os.path.join(dir_path,'dp_data.in')
            with open(path,'w') as f:
                f.write(goal)
            output.append(dp.solve(path))
                

    elif solver == 'mip':
      
        for goal in goals :
            path = os.path.join(dir_path,'mip_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(mip.solve(path))

    elif solver == 'baseline':
        
        for goal in goals :
            path = os.path.join(dir_path,'baseline_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(baseline.solve(path))
            

    elif solver=='meta':
       
        for goal in goals :
            path = os.path.join(dir_path,'heuristics_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(heuristics.solve(path))
    if len(goals)==1:
        reqs,branches = get_reqs_branches_positions(goals[0].strip())
        i = 1 
        edges = []
        out = output[0].strip().split('\n')
        while i < len(out):
            edges.append(np.array(out[i].strip().split(' '), dtype='int64'))
            i+=1
        draw_map(branches,reqs,edges)

    
    return output
    
        
def get_reqs_branches_positions(lines_u):
    lines = lines_u.split('\n')
    arr = np.array(lines[0].strip().split(' '), dtype='int64')
    r = 1+arr[2]
    reqs = []
    i = arr[2]+arr[1]+1
    branches = []
    print(r)
    while r <1+arr[2]+arr[1]:

        potential = np.array(lines[r].strip().split(' '), dtype='int64')
        if len(potential)==4:
            reqs.append(np.array([potential[0],potential[1]]))
        r+=1

    while i < len(lines):
        potential = np.array(lines[i].strip().split(' '), dtype='int64')
        if len(potential)==4:
            branches.append(np.array([potential[0],potential[1]]))
        i+=1
    return np.array(reqs) , np.array(branches)



