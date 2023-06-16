from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from training import trainModel
from symptoms_list_generator import create_symptoms_list

def predict(symptoms):
    model = DecisionTreeClassifier()
    trainModel(model)
    symptoms_list = create_symptoms_list()

    for element in symptoms:
        symptoms_list[element] = [1]

    input_data = pd.DataFrame(symptoms_list) 
    diagnosis = model.predict(input_data)
    print('Disease: ', diagnosis[0])

    file = pd.read_csv(r'C:\Users\Pavan\Python Projects\P4\Symptom_Checker\Module\remedy.csv')

    for i in range(len(file)):
        sfile = file.values[i][0]
        dst = file.values[i][1]
        if sfile==diagnosis:
            print('Remedy: ', dst)
            break