



import os 
import dp ,baseline,mip,heuristics

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


    
    return output
    
        
def get_reqs_branches_positions(lines):
    arr = np.array(lines[0].split(' '), dtype='int64')
    r = 1+arr[2]
    reqs = []
    i = arr[2]+arr[1]
    branches = []
    while r <1+arr[2]+arr[1]:

        potential = np.array(arr[r].split(' '), dtype='int64')
        if len(potential)==4:
            reqs.append((potential[0],potential[1]))
        r+=1
    while i < len(arr):
        potential = np.array(arr[i].split(' '), dtype='int64')
        if len(potential)==4:
            branches.append((potential[0],potential[1]))
        i+=1
    



