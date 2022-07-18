import streamlit as st
from predict_page import show_prediction
from explore_page import show_explore

page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))

if page == "Predict":
    show_prediction()
else:
    show_explore()