import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Clean Country data
def balance_country(col, cutoff):
    col_map = {}
    for i in range(len(col)):
        if col.values[i] >= cutoff:
            col_map[col.index[i]] = col.index[i]
        else:
            col_map[col.index[i]]= "Other"
    return col_map

# Clean Experience data
def clean_exp(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

# Clean Education data
def clean_EdLevel(x):
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Other doctoral degree' in x or 'Professional degree' in x:
        return 'Post graduation'
    return 'Less than a Bachelors degree'

@st.cache
# Load all the data
def load_data():
    df = pd.read_csv("stack-overflow-developer-survey-2021\survey_results_public.csv")

    # Select the col
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    # And drop it as we don't want to feed in our ML model
    df = df.drop("Employment", axis=1)

    country_map = balance_country(df.Country.value_counts(), 500)
    df['Country'] = df['Country'].map(country_map)

    # There are a lot of outliers in above data
    # so, we just want to keep salary reanging from $10,000 to 250000
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_exp)
    df['EdLevel'] = df['EdLevel'].apply(clean_EdLevel)

    return df

#df = load_data()
df = pd.read_csv('Cleaned_Data.csv')
#store = df.to_csv('Cleaned_Data.csv')

def show_explore():
    st.title("Explore Software Engineer Salaries")

    st.write("""### Stack Overflow Developer Survey 2021""")
    data = df["Country"].value_counts()

    # Create the Pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=100)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    # Plot the Pie chart on Streamlit
    st.pyplot(fig1)

    # Create the bar graph
    st.write("""#### Mean Salary Based On Country""")

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    # Create the line graph
    st.write("""#### Mean Salary Based On Experience""")

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
