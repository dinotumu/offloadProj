#!/usr/bin/python3

# imports
from sklearn import linear_model
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

data_set = pd.read_csv(r'/home/dinotumu/Documents/offloadProj/trainmodel_cloud_offloadProj/data/csv_local_exec_time/0.57.38_4.4.2019.csv')
df = pd.DataFrame(data_set,columns=['file_name', 'time_stamp', 'input_size', 'execution_time', 'average_cpu_util'])

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


X = df[['input_size', 'average_cpu_util']].values.reshape(-1,1) 
Y = df['execution_time'].values.reshape(-1,1)
 
# Using scikit learn for linear regression
regression_model = linear_model.LinearRegression()
regression_model.fit(X, Y)

print('Intercept: \n', regression_model.intercept_)
print('Coefficients: \n', regression_model.coef_)


# prediction for new input values using the model
input_ = [[1233, 89]]
print ('Predicted Execution time: \n', regression_model.predict(input_) )
