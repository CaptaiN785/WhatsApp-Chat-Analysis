import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import seaborn as sns
import re

## Function to find mobile number and names
def find_sender(x):
    pattern = "^\s-\s([\w\s\d+]+):"
    res = re.search(pattern, x)
    if res == None:
        return ""
    else:
        return res[1]

## Function to preprocess the data
def data_preprocessing(file_path):
    ## Loading chat data
    file = open(file_path)
    data = file.read()
    pattern = "\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s.M"

    message = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'date':dates, "message":message})

    df['date'] = pd.to_datetime(df['date'].str.replace(',',''))

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['sender'] = df['message'].apply(lambda x : find_sender(x))

    indices = df[df['sender'] == ""].index
    df.drop(indices, inplace = True)

    pattern = "^\s-\s[\w\s\d+]+:"
    df['text'] = df['message'].apply(lambda x : re.split(pattern, x)[1])\
                .str.replace('\\n','').str.strip().str.lower()

    df.drop(['date','message'], axis=1, inplace=True)
    return df

