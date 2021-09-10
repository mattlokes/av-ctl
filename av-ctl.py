from flask import Flask, request
from flask_restful import Resource, Api

from config import *

from controllers.matrix_ctl import *

app = Flask(__name__)
api = Api(app)

cfg = Config('config.yaml')

matrix_ctl = MatrixCtl(cfg)

class MatrixCtlResource(Resource):
    def get(self, target, cmd):
        print("target: {} | cmd: {}".format(target, cmd))
        return {}

    def put(self, target, cmd):
        print("target: {} | cmd: {}".format(target, cmd))
        cmd_args = request.form['data']
        return {}

api.add_resource(MatrixCtlResource, '/matrix/<string:target>/<string:cmd>')

if __name__ == '__main__':
    app.run(debug=True)
