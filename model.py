import constants
import csv
# import Excel as xl
# import numpy as np


def Get_Questions_And_Answers():  # -> (list[str], dict[list[str]])
    """
    Returns a list of questions and a dictionary with the question as the key and a list of answers as the value
    """
    with open('QuestionProfiles.csv') as file:  # Opens the file with the questions and answers
        reader = csv.reader(file)  # Creates a reader object
        current = None  # Initialize
        answers = {}  # Initialize
        questions = []  # Initialize
        for row in reader:  # For Each Row in the file
            if row[0]:  # If the first column of the row has a value
                current = row[0]  # Set current to the value of the first column
                questions.append(current)  # append the first column/current question, to the list of questions
                answers[current] = []  # Initialize the list of answers to the current question
            answers[current].append(row[1])  # Add the answer to the question
    return questions, answers  # Return questions and answers

def diagnose(questions, answers):
    """
    Takes in questions and answers and the answers to the questions, then returns a link to the a google docs sheet with
    data on the given diagnosis.
    """
    links = {
        '1': 'https://docs.google.com/presentation/d/1cUBc5G1JMNM3qHb20wA3PAzc4kowVDpfTHVv_OD7nVk/edit?usp=sharing',
        '2': 'https://docs.google.com/presentation/d/1lF5JwR-ZaNiGYCVjsMEocCmfuwl2pkU5pZ30v6Ha0wM/edit?usp=sharing',
        '3': 'https://docs.google.com/presentation/d/1APkxgELr0ay-4n6Tq0N1-CjylpwwPuhVZu_qCV90Ai0/edit?usp=sharing',
        '4': 'https://docs.google.com/presentation/d/1APkxgELr0ay-4n6Tq0N1-CjylpwwPuhVZu_qCV90Ai0/edit?usp=sharing'
    }  # Dictionary with links the the google docs for each of the given links
    # Note if the links to the google docs change, we need to edit the Links dictionary!!
    with open('QuestionProfiles.csv') as file:  # Open the question profile
        reader = csv.reader(file)
        num_classes = 0  # Initialize the number of classes
        for line in reader:  # Count the number of classes
            num_classes = max(len(line), num_classes)  # Num classes will be the row with the most columns
        num_classes -= 2  # Subtract 2 to make up for the first 2 columns
        file.seek(0)  # Return to the start of the file
        classes = [0 for _ in range(num_classes)]
        for row in reader:  # Diagnose the user using the answers they gave and the data in the CSV file
            if row[0]:  # If this row has a value in column 1, a question
                current = row[0]  # Set current to the question/value in column 1
            if row[1] == answers[current]:  # If this row has the answer the user chose
                for i in range(num_classes):  # For each profile/class
                    classes[i] += float(row[2+i])  # Add the value in the csv to each profiles total
    profile = str(classes.index(max(classes)) + 1)  # Find the diagnosis profile with the max value, then get the
    # number for it. This is the most likely diagnosis.
    return links[profile]  # Return the link to the document containing information on the diagnosis


