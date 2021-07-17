import matplotlib.pyplot as plt 
import os 
import numpy as np
def draw_map(branches,reqs,edges):
    os.makedirs('maps',exist_ok=True)
    colors ={
        'R':'#33BEFF',
        'B':'#139C3E',
    }
    print(branches)
    branches_x = branches[:,0]
    branches_y = branches[:,1]
    reqs_x = reqs[:,0]
    reqs_y = reqs[:,1]

    plt.scatter(branches_x,branches_y,color=colors.get('B'))
    plt.scatter(reqs_x,reqs_y,color=colors.get('R'))
    i = 0 
    while i < len(branches_x):
        plt.text(branches_x[i],branches_y[i],f'Branch {i+1}')
        i+=1
    i=0
    while i < len(reqs_x):
        plt.text(reqs_x[i],reqs_y[i],f'Request {i+1}')
        i+=1
    
    for e in edges:

        plt.plot([reqs_x[e[0]-1],branches_x[e[1]-1]],[reqs_y[e[0]-1],branches_y[e[1]-1]],color='#00FF00')
        x = (reqs_x[e[0]-1]+branches_x[e[1]-1])/2
        y = (reqs_y[e[0]-1]+branches_y[e[1]-1])/2
        plt.text(x,y,f'Slot {e[2]}\nCounter {e[3]}')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig('./maps/im.png')
    plt.close()


    

