import streamlit as st
import pickle
import numpy as np

def load_model():
    with open("save_model.pkl", 'rb') as file:
        data = pickle.load(file)
    return data

# Load the model
data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_edu = data["le_edu"]

def show_prediction():
    st.title("SWE Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    # Create the dropbox for COuntry and Education
    countries = (
        "United States of America",
        'India',
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'Canada',
        'France',
        'Brazil',
        'Spain',
        'Netherlands',
        'Australia',
        'Poland',
        'Italy',
        'Russian Federation',
        'Sweden',
    )

    education = (
        "Master’s degree",
        "Bachelor’s degree",
        "Post graduation",
        "Less than a Bachelors degree",
    )
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    # Create slider for Experience
    exp = st.slider("Years os Experience", 0, 50, 3) # Range is 0 to 50 and default val is 3

    # Create the Prediction Button
    btn = st.button("Predict Salary")

    if btn:
        x = np.array([[country, education, exp]])
        x[:, 0] = le_country.transform(x[:, 0])
        x[:, 1] = le_edu.transform(x[:, 1])
        x = x.astype(float)

        salary = regressor.predict(x)
        # Display the prediction
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")