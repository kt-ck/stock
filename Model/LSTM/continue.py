import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import time

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

regressor = load_model("model_2022-4-11-15-17.h5")
X_train = np.load("X_train.npy")
y_train = np.load("y_train.npy")
regressor.fit(X_train, y_train, epochs=100, batch_size=32)


now_obj = time.localtime()
year = now_obj.tm_year
month= now_obj.tm_mon
day = now_obj.tm_mday
hour = now_obj.tm_hour
minite = now_obj.tm_min

now = '{}-{}-{}-{}-{}'.format(year, month, day, hour, minite)
regressor.save("mv1_{}.h5".format(now))

