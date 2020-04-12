from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import pymysql


def predict_humidity(periods):

    # Open database connection
    db = pymysql.connect("weather_prediction_db","root","admin","admin" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    cursor.execute("SELECT * FROM admin.historical_data")

    # Fetch a single row using fetchone() method.
    db_data = cursor.fetchall()

    db.close()    
    
    df = pd.DataFrame(db_data, columns =['id','measure_date', 'temperature', 'humidity'])
    #df = pd.read_csv('humidity_min_clean.csv', names=['datetime','san_francisco'], header=0)
    
    model = pm.auto_arima(df.humidity, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
    # Forecast
    n_periods = periods # Days
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
    # fc contains the forecasting for the next 24 hours.
    return fc