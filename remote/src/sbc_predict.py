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

data_set = pd.read_csv(r'/home/dinotumu/Documents/offloadProj/remote/data/sbc_train_dataset/25.4.2019_11.20.6.csv')
df = pd.DataFrame(data_set,columns=['file_name', 'input_size', 'average_cpu_util', 'execution_time'])

# print (df)

# print(data_set.shape)
# print(data_set.describe())


# # Checking for linearity for input_size
# plt.scatter(df['input_size'], df['execution_time'], color='red')
# plt.title('Execution Time Vs Input Size', fontsize=14)
# plt.xlabel('Input Size', fontsize=14)
# plt.ylabel('Execution Time', fontsize=14)
# plt.grid(True)
# plt.show()

# # Checking for linearity for average_cpu_util
# plt.scatter(df['average_cpu_util'], df['execution_time'], color='red')
# plt.title('Execution Time Vs Average CPU Utilization', fontsize=14)
# plt.xlabel('Input Size', fontsize=14)
# plt.ylabel('Average CPU Utilization', fontsize=14)
# plt.grid(True)
# plt.show()


X = df[['input_size', 'average_cpu_util']].values
Y = df['execution_time'].values
 
# Using scikit learn for linear regression
regression_model = linear_model.LinearRegression()
regression_model.fit(X, Y)

print('Intercept: \n', regression_model.intercept_)
print('Coefficients: \n', regression_model.coef_)


# prediction for new input values using the model
input_ = [[2633, 0.98]]
print ('Predicted Execution time: \n', regression_model.predict(input_) )


# Y_pred = regression_model.predict(X_test)

# print(metrics.mean_absolute_error(y_true, y_pred))
# print(metrics.mean_squared_error(y_true, y_pred))
# print(np.sqrt(metrics.mean_squared_error(y_true, y_pred)))

# print(X_test)
# print(Y_test)
# print(Y_pred)