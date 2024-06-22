import numpy as np
import pandas as pd
import pickle
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

data = pd.read_csv("E:\\Courses\\Stroke-Prediction-Test\\predict\\hypertension.csv")
# print(data)

# Split the dataset into training and testing sets
X = data.drop("hypertension", axis=1)
y = data["hypertension"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Create a logistic regression model
model = LogisticRegression(random_state=0)

# Train the logistic regression model
model.fit(X_train, y_train)


# Predict the hypertension class for the testing set
y_pred = model.predict(X_test)

# Evaluate the performance of the logistic regression model
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
false_positives = conf_matrix[0, 1]
false_negatives = conf_matrix[1, 0]


# predict_data = pd.DataFrame([[81]] , columns=['heart_pulses'])
# result = model.predict(predict_data)
# print(result)

# print("Accuracy:", accuracy)
# print("Precision:", precision)
# print("Recall:", recall)
# print("F1-score:", f1)
# print("False positives:", false_positives)
# print("False negatives:", false_negatives)

with open('heart_pulses_hypertension_model.pkl', 'wb') as f:
    pickle.dump(model, f)