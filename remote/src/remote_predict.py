#!/usr/bin/python3

# imports
import os
import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

PWD = os.getcwd()
REMOTE_PREDICT = PWD + '/sbc' + '/data/remote_model.csv'

data_set = pd.read_csv(r'/home/dinotumu/Documents/offloadProj/remote/data/remote_train_dataset/10.4.2019_7.45.8.csv')
df = pd.DataFrame(data_set,columns=['file_name', 'time_stamp', 'input_size', 'execution_time'])

print (df)
# print(data_set.shape)
# print(data_set.describe())

# # Checking for linearity for input_size
# plt.scatter(df['input_size'], df['execution_time'], color='red')
# plt.title('Execution Time Vs Input Size', fontsize=14)
# plt.xlabel('Input Size', fontsize=14)
# plt.ylabel('Execution Time', fontsize=14)
# plt.grid(True)
# plt.show()

X = df['input_size'].values.reshape(-1,1) 
Y = df['execution_time'].values.reshape(-1,1)
 
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

# Using scikit learn for linear regression
regression_model = linear_model.LinearRegression()
regression_model.fit(X, Y)
# regression_model.fit(X_train, Y_train)

print('Intercept: \n', format(float(regression_model.intercept_), '.10f'))
print('Coefficients: \n', format(float(regression_model.coef_), '.10f'))


# # prediction for new input values using the model
# input_size = [[1233], [76653]]
# print ('Predicted Execution time: \n', regression_model.predict(input_size) )

# Y_pred = regression_model.predict(X_test)

# print(metrics.mean_absolute_error(y_true, y_pred))
# print(metrics.mean_squared_error(y_true, y_pred))
# print(np.sqrt(metrics.mean_squared_error(y_true, y_pred)))

# print(X_test)
# print(Y_test)
# print(Y_pred)

# with open(REMOTE_PREDICT) as remote:
#     r_coeff1, r_coeff2 = [float(i) for i in remote.readline()[:-1].split(',')]
# print( r_coeff1 * 1233 + r_coeff2)
# print( r_coeff1 * 76653 + r_coeff2)