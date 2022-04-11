from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

csv_path = "../../testdata/600519.csv"
col_name = ["actPreClosePrice",
            "openPrice",
            "highestPrice",
            "lowestPrice",
            "closePrice",
            "turnoverVol",
            "turnoverValue",
            "dealAmount",
            "turnoverRate",
            "negMarketValue",
            "marketValue",
            "chgPct",
            "PE",
            "PE1",
            "PB",
            "vwap"
            ]


dataset_test = pd.read_csv(csv_path,encoding='gbk')
# use open stock column, choose right col
test_set = dataset_test[col_name].iloc[-90:,].values

scaler = joblib.load("scaler_2022-4-11-16-29")
inputs = scaler.transform(test_set)


X_test = np.array([inputs])

regressor = load_model("model_2022-4-11-16-29.h5")
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

show_obj = {}

for index in range(len(col_name)):
    show_obj[col_name[index]] = predicted_stock_price[0][index]
print(show_obj)