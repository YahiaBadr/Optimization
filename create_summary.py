import dp, mip, heuristics,baseline,sys,os
import pandas as pd 

import time 

# def create_dirs(dir_path):
#     dir_path = dir_path+'_output'
#     os.makedirs(dir_path,exist_ok=True)
#     Algo1dir = os.path.join(dir_path,'Algo1')
#     Algo2dir = os.path.join(dir_path,'Algo2')
#     Algo3dir = os.path.join(dir_path,'Algo3')
#     Algo4dir = os.path.join(dir_path,'Algo4')


#     os.makedirs(Algo1dir,exist_ok=True)
#     os.makedirs(Algo2dir,exist_ok=True)
#     os.makedirs(Algo3dir,exist_ok=True)
#     os.makedirs(Algo4dir,exist_ok=True)

#     return dir_path



def solve_baseline(path,folderName,filename):

    start_time = time.time()
    matches, _ = baseline.baselineSolution(path)
    duration_time= time.time() - start_time
    return matches,duration_time

def solve_heuristics(path,folderName,filename):
    start_time = time.time()
    matches, _ = heuristics.HeuristicSolution(path)
    duration_time= time.time() - start_time
    return matches,duration_time

def solve_dp(path,folderName,filename):

    start_time = time.time()
    matches ,_= dp.dpSolution(path)
    duration_time= time.time() - start_time
    return matches,duration_time


def solve_mip(path,folderName,filename):
    start_time = time.time()
    try:
        matches, _ = mip.MIPSolution(path)
    except:
        matches = 0
    duration_time= time.time() - start_time
    return matches,duration_time

if __name__=='__main__':
    folderName = sys.argv[1] 
    dir_path = dir_path+'_output'
    os.makedirs(dir_path,exist_ok=True)
    summary_df = pd.DataFrame(columns=['test_case', 'n', 'c', 'algo1_z', 'algo1_t', 'algo2_z', 'algo2_t',  'algo3_z', 'algo3_t', 'algo4_z', 'algo4_t'])
    summary_dir =os.path.join(dir_path,'summary.csv')

    for filename in sorted(os.listdir("./"+folderName), key = lambda x: int(x.split("_")[1].split(".")[0])):
        testnum = int(filename[5:len(filename)-3])
        path = "./" + folderName + "/" + filename
        
        z_dp,t_dp =solve_dp(path,folderName,filename)
        z_mip,t_mip =solve_mip(path,folderName,filename)
        z_baseline,t_baseline =solve_baseline(path,folderName,filename)
        z_heuristics,t_heuristics =solve_heuristics(path,folderName,filename)

        
        print(filename+' Done')
        
    
        # new_row = {'test_case':test_case,
        # 'n':inputs[0],
        # 'c':inputs[1], 
        # 'algo1_z':algo1_z, 
        # 'algo1_t':algo1_t,
        # 'algo2_z':algo2_z, 
        # 'algo2_t':algo2_t,  
        # 'algo3_z':algo3_z, 
        # 'algo3_t':algo3_t, 
        # 'algo4_z':algo4_z, 
        # 'algo4_t':algo4_t
        # }
        # summary_df = summary_df.append(new_row, ignore_index=True)
    summary_df.to_csv(summary_dir,index=False)