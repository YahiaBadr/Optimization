



from flask import Flask, request 

import solvers





app = Flask (__name__)

@app.route('/')
def index():
   return "Black Opt Backend Server"


@app.route('/baseline',methods=['POST','GET'])
def solve_baseline():
    if request.method =='GET':
        return "This the Baseline Solution"
    req = request.get_json(force=True)
    return solvers.solve('baseline',req['data'])

@app.route('/mip',methods=['POST','GET'])
def solve_mip():
    if request.method =='GET':
        return "This the MIP Solution"
    req = request.get_json(force=True)
    solvers.solve('mip',req['data'])
    return "mip"



@app.route('/dp',methods=['POST','GET'])
def solve_dp():
    if request.method =='GET':
        return "This the DP Solution"
    req = request.get_json(force=True)
    return solvers.solve('dp',req['data'])
    


@app.route('/meta',methods=['POST','GET'])
def solve_meta():
    if request.method =='GET':
        return "This the Meta Solution"
    req = request.get_json(force=True)
    solvers.solve('meta',req['data'])
    return "meta"



if __name__=="__main__":
    app.run(debug=True)