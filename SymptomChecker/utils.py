import pandas as pd

def at_least_one(list):
    result = 0
    for item in list:
        result = result or item
    return result


def get_data(data):
    for col in data.columns:
        if col == "Disease": continue
        newSet = pd.get_dummies(data[col])
        data = pd.concat([data, newSet], axis=1)
        data.drop(col, axis=1, inplace=True)

    for col in data.columns:
        if type(data[col]) is not pd.Series:
            data[col] = data[col].apply(lambda x: at_least_one(x.values), axis=1)

    data = data.loc[:, ~data.columns.duplicated()]
    return data