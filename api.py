from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Prediction24(Resource):
    def get(self):
        return [{"hour":"13:10","temp":"31.20","hum":"86.30"}]

api.add_resource(Prediction24, '/servicio/v1/prediccion/24horas/')

if __name__ == '__main__':
    app.run(debug=True)