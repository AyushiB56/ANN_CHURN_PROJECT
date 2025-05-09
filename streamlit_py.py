# -*- coding: utf-8 -*-
"""streamlit.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1onT2_EjXlAI_bF2DWB12Z5L_6xeruuis
"""

import pandas as pd
import pickle
import streamlit as st

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras import regularizers
from tensorflow.keras.models import load_model

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

model = load_model("model2_regularization.h5")

with open("geo_encoder",'rb') as file:
  geo_encoder= pickle.load(file)


with open("label_encoder",'rb') as file:
  label_encoder= pickle.load(file)


with open("standard_scalar",'rb') as file:
  standard_scalar= pickle.load(file)

st.title("Customer Churn Prediction")

geo_encoder.categories_[0]

Geography= st.selectbox("Geography",geo_encoder.categories_[0])
CreditScore= st.number_input("Credit Score")
Gender= st.selectbox("Gender",label_encoder.classes_)
Age= st.number_input("Age")
Tenure = st.slider("Tenure",1,10)
Balance=st.number_input("Balance")
NumOfProducts = st.slider("Number Of Products",1,10)
HasCrCard = st.selectbox("Has Credit Card",[1,0])
IsActiveMember = st.selectbox("Is Active Member",[1,0])
EstimatedSalary=st.number_input("Estimated Salary")

# predict this
input_data = {
    'CreditScore': CreditScore,
    'Geography': Geography,
    'Gender': Gender,
    'Age': Age,
    'Tenure': Tenure,
    'Balance': Balance,
    'NumOfProducts': NumOfProducts,
    'HasCrCard': HasCrCard,
    'IsActiveMember': IsActiveMember,
    'EstimatedSalary': EstimatedSalary
}

prediction_input= pd.DataFrame([input_data])

geo_encoder_df= geo_encoder.transform([[input_data["Geography"]]]).toarray()

geo_df= pd.DataFrame(geo_encoder_df, columns= geo_encoder.get_feature_names_out(['Geography']))

prediction_input['Gender']= label_encoder.transform(prediction_input['Gender'])

prediction_input= prediction_input.drop('Geography', axis=1)

testing_data= pd.concat([prediction_input,geo_df],axis=1)

testing_data= standard_scalar.transform(testing_data)

prediction = model.predict(testing_data)

if prediction[0][0].item() >0.5:
  st.write("patient is likely to churn")
else:
  st.write("patient is not likely to churn")

