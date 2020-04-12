from flask import Flask
from flask_restful import Resource, Api
import humidity
import temperature
import time
import json
import numpy


app = Flask(__name__)
api = Api(app)


def prediction_service(periods):

    humidity_values = humidity.predict_humidity(periods)
    temperature_values = temperature.predict_temperature(periods)

    array = numpy.array(temperature_values)
    temperature_values_celcius = array - 273.15

    t0 = time.time()
    current_time = time.strftime("%H:%M",time.localtime(t0))

    list = [{"hour":current_time,"temp":temperature_values_celcius[0],"hum":humidity_values[0]}]
    for x in range(1, periods):
        tn = t0 + 60*60 * x
        ntime = time.strftime("%H:%M",time.localtime(tn))
        list.append({"hour": ntime,"temp":temperature_values_celcius[x],"hum":humidity_values[x]})
            
    return list

class PredictionSaludo(Resource):
    def get(self):
        return "Congratulations!! Welcome to prediction API!!"

api.add_resource(PredictionSaludo, '/servicio/v1/prediccion/saludo')


class Prediction24(Resource):
    def get(self):
        json = prediction_service(24)
        return json

api.add_resource(Prediction24, '/servicio/v1/prediccion/24horas')

class Prediction48(Resource):
    def get(self):
        json = prediction_service(48)
        return json

api.add_resource(Prediction48, '/servicio/v1/prediccion/48horas')

class Prediction72(Resource):
    def get(self):
        json = prediction_service(24)
        return json

api.add_resource(Prediction72, '/servicio/v1/prediccion/72horas/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')