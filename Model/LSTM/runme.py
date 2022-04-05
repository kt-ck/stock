from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

csv_path = ""
col_index = 1
train_num = 1258
unit = 60
col_name = "Open"

dataset_train = pd.read_csv(csv_path)

# use open stock column, choose right col
training_set = dataset_train.iloc[:, col_index:col_index+1].values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_training_set = scaler.fit_transform(training_set)

X_train = []
y_train = []

for i in range(unit, train_num):
    X_train.append(scaled_training_set[i-unit:i, 0])
    y_train.append(scaled_training_set[i, 0])

X_train = np.array(X_train)
y_train = np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1]), 1)

regressor = Sequential()
regressor.add(LSTM(units=50, return_sequences=True,
              input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))
regressor.compile(optimizer='adam', loss='mean_squared_error')
regressor.fit(X_train, y_train, epochs=100, batch_size=32)

# get predict csv

dataset_test = pd.read_csv("")
actual_stock_price = dataset_test.iloc[:, col_index:col_index+1].values

dataset_total = pd.concat(
    (dataset_train[col_name], dataset_test[col_name]), axis=0)
inputs = dataset_total[len(dataset_total)-len(dataset_test)-60:].values

inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)

X_test = []

for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
