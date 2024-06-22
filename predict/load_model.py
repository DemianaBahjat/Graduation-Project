import pickle
import pandas as pd

with open('X:\\Stroke\\Stroke-Prediction\\predict\\sklearn_stroke_model.pkl', 'rb') as f:
    model = pickle.load(f)

new_data = pd.DataFrame([[1, 57.0, 1, 0, 1, 100.69, 30.8]], columns=[
                        'gender', 'age', 'hypertension', 'heart_disease', 'work_type', 'avg_glucose_level', 'bmi'])

result = model.predict(new_data)
result_proba = model.predict_proba(new_data)
result_yes = result_proba[:, 1]
result_no = result_proba[:, 0]
print("Result : ", result)
print("Result Probablities : " , result_proba)
if result_yes > 0.5:
    print("You have a danger of stroke : {:.2%}".format(float(result_yes)))
else:
    print("You don't have a probability of stroke")
