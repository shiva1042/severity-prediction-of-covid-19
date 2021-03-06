# -*- coding: utf-8 -*-
"""IML_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1foXZxkb3BVIevmEekWmb_4iWgBsIhU4h
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
sns.set(rc={'figure.figsize':(14,8)}, font_scale=.9)

df = pd.read_csv('Cleaned-Data.csv')
display(df)

indicators = ['Fever', 'Tiredness', 'Dry-Cough',  'Difficulty-in-Breathing', 'Sore-Throat', 'Pains', 'Nasal-Congestion',
              'Runny-Nose', 'Diarrhea', 'Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+', 'Gender_Male',
              'Gender_Female', 'Gender_Transgender']
target_columns = ['Severity_None']
indicators2 = ['Fever', 'Tiredness', 'Dry-Cough',  'Difficulty-in-Breathing', 'Sore-Throat', 'Pains', 'Nasal-Congestion',
              'Runny-Nose', 'Diarrhea', 'Age_0-9', 'Age_10-19', 'Age_20-24', 'Age_25-59', 'Age_60+', 'Gender_Male',
              'Gender_Female', 'Gender_Transgender', 'Severity_None']
features = df[indicators]
targets = df[target_columns]
display(features.head(), targets.head())

targets = targets.rename(columns={'Severity_None':'Non_Severe'})
sns.countplot(targets['Non_Severe'])
plt.title("Severity Data Distribution")
plt.show()

temp = []
for i in indicators:
    temp.append(sum(features[i].values))
temp_df = pd.DataFrame({"Indicator":indicators, "Occurence_Count":temp})
sns.barplot(data = temp_df, y="Indicator", x="Occurence_Count")

plt.pie(data=temp_df, x="Occurence_Count", labels=temp_df["Indicator"])
plt.show()

def get_symptom_count(the_list):
    return sum(the_list.values)
features['Total_Symptom'] = features[indicators].apply(get_symptom_count, axis=1)
feats = df[indicators2]
feats['Total_Symptom'] = feats[indicators].apply(get_symptom_count, axis=1)
print(feats['Total_Symptom'])

sns.countplot(data=feats, x='Total_Symptom', hue='Severity_None')
plt.xlabel("Total symptom occurence on someone")
plt.show()

data = features
data['Non_Severe'] = targets['Non_Severe'].values
data

data_for_corr = data.drop(labels="Total_Symptom", axis=1)
# data_for_corr['Condition'] = data_for_corr['Condition'].apply(make_condition_grade)
corrmat = data_for_corr.corr()
k = 22
cols = corrmat.nlargest(k, 'Non_Severe')['Non_Severe'].index
cm = np.corrcoef(data_for_corr[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

x = data.drop(['Non_Severe', 'Total_Symptom'], axis=1)
x = PCA(n_components = 3).fit_transform(x) # no change with 5
y = data['Non_Severe']
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=.25)
x

rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)
y_predict = rfc.predict(x_test)
from sklearn.metrics import plot_roc_curve
plot_roc_curve(rfc,x_test,y_test)
plt.show()
rfc.score(x_test, y_test)

lr = LogisticRegression()
lr.fit(x_train, y_train)
from sklearn.metrics import plot_roc_curve
plot_roc_curve(lr,x_test,y_test)
plt.show()
lr.score(x_test, y_test)

DTC = DecisionTreeClassifier()
DTC.fit(x_train, y_train)
from sklearn.metrics import plot_roc_curve
plot_roc_curve(DTC,x_test,y_test)
plt.show()
DTC.score(x_test, y_test)

"""params = {
    "max_depth":[15,20,25], 
    "n_estimators":[27,30,33],
    "criterion":["gini", "entropy"],
}

rfc = RandomForestClassifier()

rf_reg = GridSearchCV(rfc, params, cv = 10, n_jobs =10)
rf_reg.fit(x_train, y_train)
print(rf_reg.best_estimator_)"""

rfc_tune = RandomForestClassifier(max_depth=15, n_estimators=27)
rfc_tune.fit(x_train, y_train)
score = cross_val_score(rfc,x_test,y_test,cv = k_fold,n_jobs=1,scoring="accuracy")
print(score.mean())

lr_tune = LogisticRegression(penalty='l1', solver='liblinear')
lr_tune.fit(x_train, y_train)
score = cross_val_score(lr_tune, x_test, y_test, cv=k_fold, n_jobs=1, scoring="accuracy")
print(score.mean())

params = {
    "criterion":["gini", "entropy"],
    "max_depth":[15,20,25], 
}
dtc = DecisionTreeClassifier()
dtc_reg = GridSearchCV(dtc, params, cv=10, n_jobs=10)
dtc_reg.fit(x_train, y_train)
print(dtc_reg.best_estimator_)

dtc_tune = DecisionTreeClassifier(max_depth=15)
dtc_tune.fit(x_train, y_train)
score = cross_val_score(dtc_tune, x_test, y_test, cv=k_fold, n_jobs=1, scoring="accuracy")
print(score.mean())

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(x_train, y_train)
score = cross_val_score(classifier, x_test, y_test, cv=k_fold, n_jobs=1, scoring="accuracy")
print(score.mean())