



import os 
# import dp , mip, baseline



def solve(solver,goal): 
    dir_path = 'web_output'
    os.makedirs(dir_path,exist_ok=True)
    if solver == 'dp':
        file_path = 'dp_output'
        with open(file_path,'w') as f:
            f.write(goal+'\n')
    elif solver == 'mip':
        file_path = 'mip_output'
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    elif solver == 'baseline':
        file_path = 'baseline_output'
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    elif solver=='meta':
        file_path = 'meta_output'
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    
        
