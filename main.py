import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

df = pd.read_csv('CO2_Emission.csv')
#df.head()

cdf = df[['ENGINESIZE','CYLINDERS','CO2EMISSION']]
#cdf.hist()
#cdf.head()

msk = np.random.rand(len(df))<0.8
train = cdf[msk]
test = cdf[~msk]

train_x = np.asanyarray(train[['ENGINESIZE']])
train_y = np.asanyarray(train[['CO2EMISSION']])

test_x = np.asanyarray(test[['ENGINESIZE']])
test_y = np.asanyarray(test[['CO2EMISSION']])

from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures as pf

regr = linear_model.LinearRegression()
poly = pf(degree = 3)

train_x_poly = poly.fit_transform(train_x)
regr.fit(train_x_poly,train_y)

coef = regr.coef_
inter = regr.intercept_
#print(coef)
#print(inter)

#plt.scatter(train.ENGINESIZE,train.CO2EMISSION,color = 'blue')
#XX = np.arange(0,10,0.1)
#YY = inter[0] + coef[0][1]*XX + coef[0][2]*np.power(XX,2) + coef[0][3]*np.power(XX,3)
#plt.plot(XX,YY,color = 'red')
#plt.xlabel('Engine Size')
#plt.ylabel('CO2 Emission')

test_x_poly = poly.transform(test_x)
test_y_poly = regr.predict(test_x_poly)

MAE = np.mean(np.absolute(test_y_poly-test_y))
MSE = np.mean((test_y_poly-test_y)**2)
VS = r2_score(test_y,test_y_poly)

#print('Mean Absolute Error = ',MAE)
#print('Mean Square Error = ',MSE)
#print('Variance Square = ',VS)

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["https://wpko.github.io/Drug-Prediction-Frontend/"],
  allow_crendentails=True,
  allow_methods=["*"],
  allow_heades=["*"],
)
class PredictionInput(BaseModel):
  ENGINESIZE: float

@app.post("/predict")
def predict(input_data: PredictionInput):
  features = [[input_data.ENGINESIZE]]
  test_x_poly1 = poly.transform(features)
  prediction = regr.predict(test_x_poly1)
  return{"prediction":str(prediction[0])}  
