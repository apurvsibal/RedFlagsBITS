from utils import get_data
import pandas
 
csvFile = pandas.read_csv(r'C:\Users\Pranav\Desktop\RedFlagsBITS-1 - Copy\SymptomChecker\dataset.csv')

def create_symptoms_list():
    train_data = get_data(csvFile)

    headings = train_data.columns.tolist()
    headings.remove('Disease')
    symptoms_list = {}

    for element in headings:
        element.replace(" ", "")

    for element in headings:
        symptoms_list[element] = [0]

    return symptoms_list
