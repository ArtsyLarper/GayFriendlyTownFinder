from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn
from sklearn.metrics import r2_score
df = pd.read_csv("citydata.csv")
from sklearn.linear_model import LinearRegression
from xgboost.sklearn import XGBRegressor



#model1
# X = df.loc[:, (df.columns != 'FinalScore') & (df.columns != 'City-State')]
# y = df['FinalScore']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# regr = MLPRegressor(random_state=100, max_iter=500000).fit(X_train, y_train)

#model2
# X = df.loc[:, (df.columns == 'PercentagePHDs') | (df.columns == 'Population') | (df.columns == 'PercentageNoReligion') | (df.columns == 'PercentageEvangelicals')]
# y = df['FinalScore']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# regr = MLPRegressor(random_state=300, max_iter=500).fit(X_train, y_train)

#model3
# X = df.loc[:, (df.columns == 'PercentagePHDs') | (df.columns == 'Population') | (df.columns == 'PercentageNoReligion') | (df.columns == 'PercentageEvangelicals')]
# y = df['FinalScore']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# regr = LinearRegression().fit(X_train, y_train)

# #model4
# X = df.loc[:, (df.columns != 'FinalScore') & (df.columns != 'City-State')]
# y = df['FinalScore']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# regr = LinearRegression().fit(X_train, y_train)

#model5
X = df.loc[:, (df.columns != 'FinalScore') & (df.columns != 'City-State')]
y = df['FinalScore']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
regr = XGBRegressor().fit(X_train, y_train)

print(regr.score(X_test, y_test))
y_predicted = regr.predict(X_test)
print(r2_score(y_test, y_predicted))
print(X)
print(y_predicted)
corrMatrix = df.corr()
seaborn.heatmap(corrMatrix, annot=True)