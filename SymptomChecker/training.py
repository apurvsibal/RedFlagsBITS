import csv
from sklearn.model_selection import train_test_split
from utils import get_data
import pandas
 
csvFile = pandas.read_csv(r'C:\Users\Pranav\Desktop\RedFlagsBITS-1 - Copy\SymptomChecker\dataset.csv')
# print(csvFile)

def trainModel(model):  
    train_data = get_data(csvFile)
    X, y = train_data.drop("Disease", axis=1), train_data['Disease']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0003)

    # Train
    model.fit(X_train, y_train)

    # Prediction
    predictions = model.predict(X_test)