



import os 
# import dp , mip, baseline



def solve(solver,goal): 
    dir_path = 'web_output'
    os.makedirs(dir_path,exist_ok=True)
    
    if solver == 'dp':
        file_path = os.path.join(dir_path,'dp_output.out')
        with open(file_path,'w') as f:
            f.write(goal+'\n')
    
    elif solver == 'mip':
        file_path = os.path.join(dir_path,'mip_output.out')
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    
    elif solver == 'baseline':
        file_path = os.path.join(dir_path,'baseline_output.out')
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    
    elif solver=='meta':
        file_path = os.path.join(dir_path,'meta_output.out')
        with open(file_path,'w') as f:
            f.write(goal+'\n') 
    
        
