



from flask import Flask, request,jsonify,send_file
from flask_cors import CORS, cross_origin

import solvers





app = Flask (__name__,static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
   return "Black Opt Backend Server"


@app.route('/baseline',methods=['POST','GET'])
@cross_origin()
def solve_baseline():
    if request.method =='GET':
        return "This the Baseline Solution"
    req = request.get_json(force=True)
    return jsonify(solvers.solve('baseline',req['data']))

@app.route('/mip',methods=['POST','GET'])
@cross_origin()
def solve_mip():
    if request.method =='GET':
        return "This the MIP Solution"
    req = request.get_json(force=True)
    return jsonify(solvers.solve('mip',req['data']))
    



@app.route('/dp',methods=['POST','GET'])
@cross_origin()
def solve_dp():
    if request.method =='GET':
        return "This the DP Solution"
    req = request.get_json(force=True)
    return jsonify(solvers.solve('dp',req['data']))
    


@app.route('/meta',methods=['POST','GET'])
@cross_origin()
def solve_meta():
    if request.method =='GET':
        return "This the Meta Solution"
    req = request.get_json(force=True)
    return jsonify(solvers.solve('meta',req['data']))



@app.route('/visualize',methods=['GET'])
@cross_origin()
def visualize():
    return send_file('./maps/im.png')
    



if __name__=="__main__":
    app.run(debug=True)