



from flask import Flask, request 

import solvers





app = Flask (__name__)

@app.route('/')
def index():
   return "Black Opt Backend Server"


@app.route('/baseline',methods=['POST','GET'])
def solve_baseline():
    req = request.get_json(force=True)
    solvers.solve('baseline',req['data'])
    return "baseline"

@app.route('/mip',methods=['POST','GET'])
def solve_mip():
    req = request.get_json(force=True)
    solvers.solve('mip',req['data'])
    return "mip"



@app.route('/dp',methods=['POST','GET'])
def solve_dp():
    req = request.get_json(force=True)
    solvers.solve('dp',req['data'])
    return "dp"


@app.route('/meta',methods=['POST','GET'])
def solve_meta():
    req = request.get_json(force=True)
    solvers.solve('meta',req['data'])
    return "meta"



if __name__=="__main__":
    app.run(debug=True)