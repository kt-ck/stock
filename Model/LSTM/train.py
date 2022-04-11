from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
import tensorflow as tf
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
import sys
import time
import joblib
csv_path = "../../testdata/600519.csv"
col_index = 1
train_num = 1258
unit = 90
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
checkpoint_path = "train/model.ckpt"


dataset_train = pd.read_csv(csv_path,encoding='gbk')


# use open stock column, choose right col
training_set = dataset_train[col_name].values

scaler = MinMaxScaler(feature_range=(-10, 10))
scaled_training_set = scaler.fit_transform(training_set)

X_train = []
y_train = []

for i in range(unit, len(training_set)):
    X_train.append(scaled_training_set[i-unit:i,:])
    y_train.append(scaled_training_set[i, :])
    

X_train = np.array(X_train)
y_train = np.array(y_train)

print(X_train.shape)
print(y_train.shape)


regressor = Sequential()
regressor.add(LSTM(units=80, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=80, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=80, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=80))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=len(col_name)))
regressor.compile(optimizer='adam', loss='mean_squared_error')
regressor.fit(X_train, y_train, epochs=100, batch_size=32)

now_obj = time.localtime()
year = now_obj.tm_year
month= now_obj.tm_mon
day = now_obj.tm_mday
hour = now_obj.tm_hour
minite = now_obj.tm_min

now = '{}-{}-{}-{}-{}'.format(year, month, day, hour, minite)
regressor.save("model_{}.h5".format(now))
joblib.dump(scaler, 'scaler_{}'.format(now))

# get predict csv

# dataset_test = pd.read_csv("")
# actual_stock_price = dataset_test.iloc[:, col_index:col_index+1].values

# dataset_total = pd.concat(
#     (dataset_train[col_name], dataset_test[col_name]), axis=0)
# inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values

# inputs = inputs.reshape(-1, 1)
# inputs = scaler.transform(inputs)

# X_test = []

# for i in range(60, 80):
#     X_test.append(inputs[i-60:i, 0])

# X_test = np.array(X_test)
# X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# predicted_stock_price = regressor.predict(X_test)
# predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
