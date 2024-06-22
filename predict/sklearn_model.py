# Import Library
import numpy as np
import pandas as pd
import pickle

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as grid_spec
import seaborn as sns
from imblearn.over_sampling import SMOTE
import scikitplot as skplt

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import binarize
from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score, precision_score, f1_score

import warnings
from pywaffle import Waffle
warnings.filterwarnings('ignore')
# End Library

# Read the data
df = pd.read_csv(
    'E:\\Bio 4\\Documentation\\Dataset\\healthcare-dataset-stroke-data-Labeld.csv')
# print(df.head(3))


# Deal with missing values in BMI by predict them by random forest
# print(df.isnull().sum())
DT_bmi_pipe = Pipeline(steps=[
    ('scale', StandardScaler()),
    ('lr', DecisionTreeRegressor(random_state=42))])
X = df[['age', 'gender', 'bmi']].copy()
X.gender = X.gender.replace(
    {'Male': 0, 'Female': 1, 'Other': -1}).astype(np.uint8)

Missing = X[X.bmi.isna()]
X = X[~X.bmi.isna()]
Y = X.pop('bmi')
DT_bmi_pipe.fit(X, Y)
predicted_bmi = pd.Series(DT_bmi_pipe.predict(
    Missing[['age', 'gender']]), index=Missing.index)
df.loc[Missing.index, 'bmi'] = predicted_bmi
# print('Missing values: ', sum(df.isnull().sum()))


# Data Visualization
variables = [
    variable for variable in df.columns if variable not in ['id', 'stroke']]
conts = ['age', 'avg_glucose_level', 'bmi']
fig = plt.figure(figsize=(12, 12), dpi=150, facecolor='#fafafa')
gs = fig.add_gridspec(4, 3)
gs.update(wspace=0.1, hspace=0.4)
background_color = "#fafafa"
plot = 0

ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1])
ax2 = fig.add_subplot(gs[0, 2])

for row in range(0, 1):
    for col in range(0, 3):
        locals()["ax"+str(plot)] = fig.add_subplot(gs[row, col])
        locals()["ax"+str(plot)].set_facecolor(background_color)
        locals()["ax"+str(plot)].tick_params(axis='y', left=False)
        locals()["ax"+str(plot)].get_yaxis().set_visible(False)
        for s in ["top", "right", "left"]:
            locals()["ax"+str(plot)].spines[s].set_visible(False)
        plot += 1

plot = 0

s = df[df['stroke'] == 1]
ns = df[df['stroke'] == 0]

for feature in conts:
    sns.kdeplot(s[feature], ax=locals()["ax"+str(plot)], color='#0f4c81',
                shade=True, linewidth=1.5, ec='black', alpha=0.9, zorder=3, legend=False)
    sns.kdeplot(ns[feature], ax=locals()["ax"+str(plot)], color='#9bb7d4',
                shade=True, linewidth=1.5, ec='black', alpha=0.9, zorder=3, legend=False)
    locals()["ax"+str(plot)].grid(which='major', axis='x',
                                  zorder=0, color='gray', linestyle=':', dashes=(1, 5))
    plot += 1

ax0.set_xlabel('Age')
ax1.set_xlabel('Avg. Glucose Levels')
ax2.set_xlabel('BMI')

ax0.text(-20, 0.056, 'Numeric Variables by Stroke & No Stroke',
         fontsize=20, fontweight='bold', fontfamily='serif')
ax0.text(-20, 0.05, 'Age looks to be a prominent factor - this will likely be a salient feautre in our models',
         fontsize=13, fontweight='light', fontfamily='serif')
str_only = df[df['stroke'] == 1]
no_str_only = df[df['stroke'] == 0]


fig = plt.figure(figsize=(10, 5), dpi=150, facecolor=background_color)
gs = fig.add_gridspec(2, 1)
gs.update(wspace=0.11, hspace=0.5)
ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor(background_color)


df['age'] = df['age'].astype(int)

rate = []
for i in range(df['age'].min(), df['age'].max()):
    rate.append(df[df['age'] < i]['stroke'].sum() /
                len(df[df['age'] < i]['stroke']))

sns.lineplot(data=rate, color='#0f4c81', ax=ax0)

for s in ["top", "right", "left"]:
    ax0.spines[s].set_visible(False)

ax0.tick_params(axis='both', which='major', labelsize=8)
ax0.tick_params(axis=u'both', which=u'both', length=0)

ax0.text(-3, 0.055, 'Risk Increase by Age', fontsize=18,
         fontfamily='serif', fontweight='bold')
ax0.text(-3, 0.047, 'As age increase, so too does risk of having a stroke',
         fontsize=14, fontfamily='serif')
# plt.show()


fig = plt.figure(figsize=(7, 2), dpi=150, facecolor=background_color,
                 FigureClass=Waffle,
                 rows=1,
                 values=[1, 19],
                 colors=['#0f4c81', "lightgray"],
                 characters='⬤',
                 font_size=20, vertical=True,)

fig.text(0.035, 0.78, 'People Affected by a Stroke in our dataset',
         fontfamily='serif', fontsize=15, fontweight='bold')
fig.text(0.035, 0.65,
         'This is around 1 in 20 people [249 out of 5000]', fontfamily='serif', fontsize=10)
# plt.show()


# Drop single 'Other' gender
no_str_only = no_str_only[(no_str_only['gender'] != 'Other')]


# Another Data Visualization
fig = plt.figure(figsize=(22, 15))
gs = fig.add_gridspec(3, 3)
gs.update(wspace=0.35, hspace=0.27)
ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[1, 2])
ax6 = fig.add_subplot(gs[2, 0])
ax7 = fig.add_subplot(gs[2, 1])
ax8 = fig.add_subplot(gs[2, 2])

background_color = "#f6f6f6"
fig.patch.set_facecolor(background_color)  # figure background color


# Plots

# Age


ax0.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
positive = pd.DataFrame(str_only["age"])
negative = pd.DataFrame(no_str_only["age"])
sns.kdeplot(positive["age"], ax=ax0, color="#0f4c81",
            shade=True, ec='black', label="positive")
sns.kdeplot(negative["age"], ax=ax0, color="#9bb7d4",
            shade=True, ec='black', label="negative")
# ax3.text(0.29, 13, 'Age',
#        fontsize=14, fontweight='bold', fontfamily='serif', color="#323232")
ax0.yaxis.set_major_locator(mtick.MultipleLocator(2))
ax0.set_ylabel('')
ax0.set_xlabel('')
ax0.text(-20, 0.0465, 'Age', fontsize=14, fontweight='bold',
         fontfamily='serif', color="#323232")


# Smoking
positive = pd.DataFrame(str_only["smoking_status"].value_counts())
positive["Percentage"] = positive["smoking_status"].apply(
    lambda x: x/sum(positive["smoking_status"])*100)
negative = pd.DataFrame(no_str_only["smoking_status"].value_counts())
negative["Percentage"] = negative["smoking_status"].apply(
    lambda x: x/sum(negative["smoking_status"])*100)

ax1.text(0, 4, 'Smoking Status', fontsize=14,
         fontweight='bold', fontfamily='serif', color="#323232")
ax1.barh(positive.index, positive['Percentage'],
         color="#0f4c81", zorder=3, height=0.7)
ax1.barh(negative.index, negative['Percentage'],
         color="#9bb7d4", zorder=3, ec='black', height=0.3)
ax1.xaxis.set_major_formatter(mtick.PercentFormatter())
ax1.xaxis.set_major_locator(mtick.MultipleLocator(10))

##
# Ax2 - GENDER
positive = pd.DataFrame(str_only["gender"].value_counts())
positive["Percentage"] = positive["gender"].apply(
    lambda x: x/sum(positive["gender"])*100)
negative = pd.DataFrame(no_str_only["gender"].value_counts())
negative["Percentage"] = negative["gender"].apply(
    lambda x: x/sum(negative["gender"])*100)

x = np.arange(len(positive))
ax2.text(-0.4, 68.5, 'Gender', fontsize=14, fontweight='bold',
         fontfamily='serif', color="#323232")
ax2.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
ax2.bar(x, height=positive["Percentage"], zorder=3, color="#0f4c81", width=0.4)
ax2.bar(x+0.4, height=negative["Percentage"],
        zorder=3, color="#9bb7d4", width=0.4)
ax2.set_xticks(x + 0.4 / 2)
ax2.set_xticklabels(['Male', 'Female'])
ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
ax2.yaxis.set_major_locator(mtick.MultipleLocator(10))
for i, j in zip([0, 1], positive["Percentage"]):
    ax2.annotate(f'{j:0.0f}%', xy=(i, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')
for i, j in zip([0, 1], negative["Percentage"]):
    ax2.annotate(f'{j:0.0f}%', xy=(i+0.4, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')


# Heart Dis

positive = pd.DataFrame(str_only["heart_disease"].value_counts())
positive["Percentage"] = positive["heart_disease"].apply(
    lambda x: x/sum(positive["heart_disease"])*100)
negative = pd.DataFrame(no_str_only["heart_disease"].value_counts())
negative["Percentage"] = negative["heart_disease"].apply(
    lambda x: x/sum(negative["heart_disease"])*100)

x = np.arange(len(positive))
ax3.text(-0.3, 110, 'Heart Disease', fontsize=14,
         fontweight='bold', fontfamily='serif', color="#323232")
ax3.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
ax3.bar(x, height=positive["Percentage"], zorder=3, color="#0f4c81", width=0.4)
ax3.bar(x+0.4, height=negative["Percentage"],
        zorder=3, color="#9bb7d4", width=0.4)
ax3.set_xticks(x + 0.4 / 2)
ax3.set_xticklabels(['No History', 'History'])
ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
ax3.yaxis.set_major_locator(mtick.MultipleLocator(20))
for i, j in zip([0, 1], positive["Percentage"]):
    ax3.annotate(f'{j:0.0f}%', xy=(i, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')
for i, j in zip([0, 1], negative["Percentage"]):
    ax3.annotate(f'{j:0.0f}%', xy=(i+0.4, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')


# AX4 - TITLE

ax4.spines["bottom"].set_visible(False)
ax4.tick_params(left=False, bottom=False)
ax4.set_xticklabels([])
ax4.set_yticklabels([])
ax4.text(0.5, 0.6, 'Can we see patterns for\n\n patients in our data?', horizontalalignment='center', verticalalignment='center',
         fontsize=22, fontweight='bold', fontfamily='serif', color="#323232")

ax4.text(0.15, 0.57, "Stroke", fontweight="bold",
         fontfamily='serif', fontsize=22, color='#0f4c81')
ax4.text(0.41, 0.57, "&", fontweight="bold",
         fontfamily='serif', fontsize=22, color='#323232')
ax4.text(0.49, 0.57, "No-Stroke", fontweight="bold",
         fontfamily='serif', fontsize=22, color='#9bb7d4')


# Glucose

ax5.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
positive = pd.DataFrame(str_only["avg_glucose_level"])
negative = pd.DataFrame(no_str_only["avg_glucose_level"])
sns.kdeplot(positive["avg_glucose_level"], ax=ax5,
            color="#0f4c81", ec='black', shade=True, label="positive")
sns.kdeplot(negative["avg_glucose_level"], ax=ax5,
            color="#9bb7d4", ec='black', shade=True, label="negative")
ax5.text(-55, 0.01855, 'Avg. Glucose Level',
         fontsize=14, fontweight='bold', fontfamily='serif', color="#323232")
ax5.yaxis.set_major_locator(mtick.MultipleLocator(2))
ax5.set_ylabel('')
ax5.set_xlabel('')


# BMI


ax6.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
positive = pd.DataFrame(str_only["bmi"])
negative = pd.DataFrame(no_str_only["bmi"])
sns.kdeplot(positive["bmi"], ax=ax6, color="#0f4c81",
            ec='black', shade=True, label="positive")
sns.kdeplot(negative["bmi"], ax=ax6, color="#9bb7d4",
            ec='black', shade=True, label="negative")
ax6.text(-0.06, 0.09, 'BMI',
         fontsize=14, fontweight='bold', fontfamily='serif', color="#323232")
ax6.yaxis.set_major_locator(mtick.MultipleLocator(2))
ax6.set_ylabel('')
ax6.set_xlabel('')


# Work Type

positive = pd.DataFrame(str_only["work_type"].value_counts())
positive["Percentage"] = positive["work_type"].apply(
    lambda x: x/sum(positive["work_type"])*100)
positive = positive.sort_index()

negative = pd.DataFrame(no_str_only["work_type"].value_counts())
negative["Percentage"] = negative["work_type"].apply(
    lambda x: x/sum(negative["work_type"])*100)
negative = negative.sort_index()

ax7.bar(negative.index,
        height=negative["Percentage"], zorder=3, color="#9bb7d4", width=0.05)
ax7.scatter(negative.index,
            negative["Percentage"], zorder=3, s=200, color="#9bb7d4")
ax7.bar(np.arange(len(positive.index))+0.4,
        height=positive["Percentage"], zorder=3, color="#0f4c81", width=0.05)
ax7.scatter(np.arange(len(positive.index))+0.4,
            positive["Percentage"], zorder=3, s=200, color="#0f4c81")

ax7.yaxis.set_major_formatter(mtick.PercentFormatter())
ax7.yaxis.set_major_locator(mtick.MultipleLocator(10))
ax7.set_xticks(np.arange(len(positive.index))+0.4 / 2)
ax7.set_xticklabels(list(positive.index), rotation=0)
ax7.text(-0.5, 66, 'Work Type', fontsize=14, fontweight='bold',
         fontfamily='serif', color="#323232")


# hypertension

positive = pd.DataFrame(str_only["hypertension"].value_counts())
positive["Percentage"] = positive["hypertension"].apply(
    lambda x: x/sum(positive["hypertension"])*100)
negative = pd.DataFrame(no_str_only["hypertension"].value_counts())
negative["Percentage"] = negative["hypertension"].apply(
    lambda x: x/sum(negative["hypertension"])*100)

x = np.arange(len(positive))
ax8.text(-0.45, 100, 'Hypertension', fontsize=14,
         fontweight='bold', fontfamily='serif', color="#323232")
ax8.grid(color='gray', linestyle=':', axis='y', zorder=0,  dashes=(1, 5))
ax8.bar(x, height=positive["Percentage"], zorder=3, color="#0f4c81", width=0.4)
ax8.bar(x+0.4, height=negative["Percentage"],
        zorder=3, color="#9bb7d4", width=0.4)
ax8.set_xticks(x + 0.4 / 2)
ax8.set_xticklabels(['No History', 'History'])
ax8.yaxis.set_major_formatter(mtick.PercentFormatter())
ax8.yaxis.set_major_locator(mtick.MultipleLocator(20))
for i, j in zip([0, 1], positive["Percentage"]):
    ax8.annotate(f'{j:0.0f}%', xy=(i, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')
for i, j in zip([0, 1], negative["Percentage"]):
    ax8.annotate(f'{j:0.0f}%', xy=(i+0.4, j/2), color='#f6f6f6',
                 horizontalalignment='center', verticalalignment='center')
# tidy up
for s in ["top", "right", "left"]:
    for i in range(0, 9):
        locals()["ax"+str(i)].spines[s].set_visible(False)
for i in range(0, 9):
    locals()["ax"+str(i)].set_facecolor(background_color)
    locals()["ax"+str(i)].tick_params(axis=u'both', which=u'both', length=0)
    locals()["ax"+str(i)].set_facecolor(background_color)
# plt.show()


# Encoding categorical values
df['gender'] = df['gender'].replace(
    {'Male': 0, 'Female': 1, 'Other': -1}).astype(np.uint8)
df['Residence_type'] = df['Residence_type'].replace(
    {'Rural': 0, 'Urban': 1}).astype(np.uint8)
df['work_type'] = df['work_type'].replace(
    {'Private': 0, 'Self-employed': 1, 'Govt_job': 2, 'children': -1, 'Never_worked': -2}).astype(np.uint8)


# Inverse of Null Accuracy
# print('Inverse of Null Accuracy: ',249/(249+4861))
# print('Null Accuracy: ',4861/(4861+249))


# Split the dataset into training and test data
X = df[['gender', 'age', 'hypertension', 'heart_disease',
        'work_type', 'avg_glucose_level', 'bmi']]
y = df['stroke']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.3, random_state=42)
# print(X_test.head(2))


# SMOTE Technique
oversample = SMOTE()
X_train_resh, y_train_resh = oversample.fit_resample(X_train, y_train.ravel())


# Logistic Regression Model
logreg_pipeline = Pipeline(
    steps=[('scale', StandardScaler()), ('LR', LogisticRegression(random_state=42))])
logreg_cv = cross_val_score(
    logreg_pipeline, X_train_resh, y_train_resh, cv=10, scoring='f1')
logreg_pipeline.fit(X_train_resh, y_train_resh)
logreg_pred = logreg_pipeline.predict(X_test)
logreg_cm = confusion_matrix(y_test, logreg_pred)
logreg_f1 = f1_score(y_test, logreg_pred)
penalty = ['l1', 'l2']
C = [0.001, 0.01, 0.1, 1, 10, 100]
log_param_grid = {'penalty': penalty, 'C': C}
logreg = LogisticRegression()
grid = GridSearchCV(logreg, log_param_grid)
logreg_pipeline = Pipeline(steps=[('scale', StandardScaler(
)), ('LR', LogisticRegression(C=0.1, penalty='l2', random_state=42))])
logreg_pipeline.fit(X_train_resh, y_train_resh)


# We can maniupulate the threshold that our model uses to classify stroke vs no-stroke.
for i in range(1, 6):
    cm1 = 0
    y_pred1 = logreg_pipeline.predict_proba(X_test)[:, 1]
    y_pred1 = y_pred1.reshape(-1, 1)
    y_pred2 = binarize(y_pred1, threshold=i/10)
    y_pred2 = np.where(y_pred2 == 1, 1, 0)
    cm1 = confusion_matrix(y_test, y_pred2)


# mydata = [[0, 60.0, 0, 0, 0, 100.69, 30.6]]
# logreg_tuned_pred = logreg_pipeline.predict(mydata)
# logreg_tuned_pred_proba = logreg_pipeline.predict_proba(mydata)
# print(logreg_tuned_pred)
# print(logreg_tuned_pred_proba)

with open('sklearn_stroke_model.pkl', 'wb') as f:
    pickle.dump(logreg_pipeline, f)
