# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 19:13:48 2017

@author: theaj
"""

#Reccurant Neural Networks

#Part 1- Data Preproccessing

#Importing the libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#importing the dataset
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

#Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
training_set_scaled= sc.fit_transform(training_set)

#Creating a data structure with 60 timesteps and 1 output
#at one time t, the RNN will look at 60 values before time t, and with it, it will predict t+1

X_train=[]
y_train=[]

for i in range(60, 1258 ):
    X_train.append(training_set_scaled[i-60:i,0])
    y_train.append(training_set_scaled[i,0])

X_train,y_train= np.array(X_train), np.array(y_train)     
    
#Reshaping
X_train= np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))    
    
#Part 2 -Building the RNN

#Import the keras libraries

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

#Initialising the RNN

regressor=Sequential()

#Adding the first LSTM layer and Dropout regularisation
regressor.add(LSTM(units= 50, return_sequences= True, input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(rate=0.2))

#Adding a second LSTM layer and Dropout regularisation

regressor.add(LSTM(units= 50, return_sequences= True))
regressor.add(Dropout(rate=0.2))

#Adding a third LSTM layer and Dropout regularization
regressor.add(LSTM(units= 50, return_sequences= True))
regressor.add(Dropout(rate=0.2))

#Adding a fourth LSTM layer and some Dropout regularization
regressor.add(LSTM(units= 50, return_sequences= False))
regressor.add(Dropout(rate=0.2))

#Adding the output layer

regressor.add(Dense(units=1))

#Compiling the RNN
regressor.compile(optimizer= 'adam', loss= 'mean_squared_error')

#Fitting the RNN to the Training set

regressor.fit(X_train,y_train, epochs= 100, batch_size=32)


#Part 3- Making the predictions and Visualising the resuts


#Getting the real stock price of 2017


#Getting the predicted  stock price of 2017
dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

#Getting the predicted stock price of 2017
dataset_total= pd.concat((dataset_train['Open'],dataset_test['Open']), axis=0)
inputs= dataset_total[len(dataset_total)-len(dataset_test)-60: ].values
inputs=inputs.reshape(-1,1)
inputs = sc.transform(inputs)

X_test=[]


for i in range(60, 80 ):
    X_test.append(inputs[i-60:i,0])
    

X_test= np.array(X_test) 

X_test= np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
predicted_stock_price=regressor.predict(X_test)   
predicted_stock_price=sc.inverse_transform(predicted_stock_price) 


#Visualising the result

plt.plot(real_stock_price, color='red', label= 'Real Google Stock Price')
plt.plot(predicted_stock_price, color='blue', label= 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.show()
