import streamlit as st
import pandas as pd
import numpy as np


st.title('Values drawing app')

st.subheader('Input xls/xlsx file:')
file = st.file_uploader('Choose a file')

if file is not None:
    uploaded_file = pd.ExcelFile(file)
    sheets = uploaded_file.sheet_names
    if len(sheets) > 1:
        sheet = st.selectbox('Which sheet you want to choose?',
                             options=sheets,
                             placeholder='Select sheet')
    else:
        sheet = sheets[0]
    excel_df = pd.read_excel(file, sheet_name=sheet)
    amount = st.number_input('Choose amount to draw', min_value=1)
    column = st.selectbox('From which column you want to draw from?',
                          options=excel_df.columns)
    if st.checkbox('Unique'):
        values = excel_df[column].unique()
    else:
        values = excel_df[column]

    previous = st.file_uploader('Choices to eliminate?')
    if previous is not None:
        previous_df = pd.read_csv(previous)
        values = np.asarray([i for i in values if i not in previous_df])

    if st.button('Draw'):
        drawn = np.random.choice(values, size=amount, replace=False)
        drawn = pd.DataFrame(drawn)
        st.dataframe(drawn.style.format(thousands='', ),
                     hide_index=True, column_config={1: "Values"})