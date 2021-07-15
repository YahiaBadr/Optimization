



import os 
import dp ,baseline



def solve(solver,goal): 
    dir_path = 'web_input'
    os.makedirs(dir_path,exist_ok=True)
    
    if solver == 'dp':
        path = os.path.join(dir_path,'dp_data.in')
        with open(path,'w') as f:
            f.write(goal)

        return dp.solve(path)

    
    elif solver == 'mip':
        path = os.path.join(dir_path,'mip_data.in')
        with open(path,'w') as f:
            f.write(goal+'\n') 
    
    elif solver == 'baseline':
        path = os.path.join(dir_path,'baseline_data.in')
        with open(path,'w') as f:
            f.write(goal+'\n') 
        return baseline.solve(path)

    elif solver=='meta':
        path = os.path.join(dir_path,'meta_data.in')
        with open(path,'w') as f:
            f.write(goal+'\n') 
    
        
