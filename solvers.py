



import os 
import dp ,baseline,mip,heuristics



def solve(solver,goals_u): 
    dir_path = 'web_input'
    os.makedirs(dir_path,exist_ok=True)
    
    if solver == 'dp':
        goals = goals_u.split("#")
        output = []
        for index,goal in enumerate(goals) :
            path = os.path.join(dir_path,'dp_data.in')
            with open(path,'w') as f:
                f.write(goal)
            output.append(dp.solve(path))
            # if index == len(goals)-1:
            # else:
                # output += dp.solve(path)+'#\n'
        return output

    elif solver == 'mip':
        goals = goals_u.split("#")
        output = []
        for index,goal in enumerate(goals) :
            path = os.path.join(dir_path,'mip_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(mip.solve(path))
            # if index == len(goals)-1:
            #     output += mip.solve(path)+'\n'
            # else:
            #     output += mip.solve(path)+'#\n'
        return output

    elif solver == 'baseline':
        goals = goals_u.split("#")
        output = []
        for index,goal in enumerate(goals) :
            path = os.path.join(dir_path,'baseline_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(baseline.solve(path))
            # if index == len(goals)-1:
            #     output += baseline.solve(path)+'\n'
            # else:
            #     output += baseline.solve(path)+'#\n'
        return output

    elif solver=='meta':
        goals = goals_u.split("#")
        output = []
        for index,goal in enumerate(goals) :
            path = os.path.join(dir_path,'heuristics_data.in')
            with open(path,'w') as f:
                f.write(goal+'\n') 
            output.append(heuristics.solve(path))
            # if index == len(goals)-1:
            #     output += heuristics.solve(path)+'\n'
            # else:
            #     output += heuristics.solve(path)+'#\n'
        return output 
    
        
