# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 08:39:40 2021

@author: ASUS
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("eda_data.csv")
df.columns

#choose relevant columns
df_model = df[["Rating","Size","Type of ownership", "Industry","Sector","Revenue","Avg Salary","State","Hourly",
               "Age of Company",'python_ind','excel_ind','aws_ind','spark_ind','sql_ind','Seniority',"Desc. Length"]]

#get dummy data
df_dum = pd.get_dummies(df_model)

#train test split
x = df_dum.drop(columns = "Avg Salary")
y = df_dum["Avg Salary"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 123)

#multiple linear regression
x_sm = x = sm.add_constant(x)
model = sm.OLS(y,x_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(x_train, y_train)

np.mean(cross_val_score(lm, x_train, y_train, scoring = "neg_mean_absolute_error", cv = 7))

#lasso regression
lasso = Lasso()
np.mean(cross_val_score(lasso, x_train, y_train, scoring = "neg_mean_absolute_error", cv = 7))

alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    las = Lasso(alpha = i/100)
    error.append(np.mean(cross_val_score(las, x_train, y_train, scoring = "neg_mean_absolute_error", cv = 7)))

plt.plot(alpha, error)

err = tuple(zip(alpha, error))
#alpha 0.07 has the least value of error (negative)

lasso2 = Lasso(alpha = 0.07)
np.mean(cross_val_score(lasso2, x_train, y_train, scoring = "neg_mean_absolute_error", cv = 7))

#random forest
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, x_train, y_train, scoring = "neg_mean_absolute_error", cv = 7))
#rf has the least value of error (negative)

#tune model (GridSearch cross validation)
#parameters to be tuned from RandomForestRegressor
param_grid = {"n_estimators":list(range(10,300,10)),
              "criterion":('mse','mae'),
              "max_features":('auto','sqrt','log2'),
              "max_depth":range(100,500,100)}

gs = GridSearchCV(rf, param_grid, scoring = "neg_mean_absolute_error", cv = 7)
gs.fit(x_train, y_train)
print("Best parameters : ", gs.best_params_)
print("Best score : ", gs.best_score_)

#test ensembles
pred_lm = lm.predict(x_test)
pred_lasso = lasso2.predict(x_test)
pred_rf = gs.best_estimator_.predict(x_test)

#calculate error between predicted and y_test
mean_absolute_error(y_test, pred_lm)
mean_absolute_error(y_test, pred_lasso)
mean_absolute_error(y_test, pred_rf)

#random forest model performs the best