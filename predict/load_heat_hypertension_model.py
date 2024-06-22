import pickle
import pandas as pd

with open('E:\\Courses\\Stroke-Prediction-Test\\predict\\heart_pulses_hypertension_model.pkl', 'rb') as h:
    model = pickle.load(h)

predict_data = pd.DataFrame([[85]] , columns=['heart_pulses'])
result = model.predict(predict_data)
print(result)