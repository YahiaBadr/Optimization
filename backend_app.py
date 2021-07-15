



from flask import Flask, request 

import solvers





app = Flask (__name__)

@app.route('/')
def index():
   return "Black Opt Backend Server"


@app.route('/baseline',methods=['POST','GET'])
def solve_baseline():
    solvers.solve('baseline',request.form['data'])
    return "baseline"

@app.route('/mip',methods=['POST','GET'])
def solve_mip():
    solvers.solve('mip',request.form['data'])
    return "mip"



@app.route('/dp',methods=['POST','GET'])
def solve_dp():
    solvers.solve('dp',request.form['data'])
    return "dp"


@app.route('/meta',methods=['POST','GET'])
def solve_meta():
    solvers.solve('meta',request.form['data'])
    return "meta"



if __name__=="__main__":
    app.run()