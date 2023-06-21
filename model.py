from typing import Tuple
import csv
import pandas as pd
import os

def get_red_flag_question(question_number: int) -> Tuple[str, Tuple[str], str]:
    csv_path = os.path.join(os.path.dirname(__file__), 'Moblie_MSK_Red_Flags.csv')
    df = pd.read_csv(csv_path)
    row = list(df.iloc[question_number - 1])
    question = row[0]
    answers = row[1:3]
    more_info = row[3]
    return question, answers, more_info

def Get_Questions_And_Answers():
    csv_path = os.path.join(os.path.dirname(__file__), 'QuestionProfiles.csv')
    with open(csv_path) as file:
        reader = csv.reader(file)
        current = None
        answers = {}
        questions = []
        for row in reader:
            if row[0]:
                current = row[0]
                questions.append(current)
                answers[current] = []
            answers[current].append(row[1])
    return questions, answers

def diagnose(questions, answers):
    links = {
        '1': 'https://docs.google.com/presentation/d/1cUBc5G1JMNM3qHb20wA3PAzc4kowVDpfTHVv_OD7nVk/edit?usp=sharing',
        '2': 'https://docs.google.com/presentation/d/1ZvTzRMkvk_bzaDNPCIq-XnxhGnb9ZjU_-tAo4yuKsZs/edit?usp=sharing',
        '3': 'https://docs.google.com/presentation/d/1r6Qr7hEGQztO4qXX8ogU0nRUVbbIv5dcyS0mZiAMGm0/edit?usp=sharing',
        '4': 'https://docs.google.com/presentation/d/1r6Qr7hEGQztO4qXX8ogU0nRUVbbIv5dcyS0mZiAMGm0/edit?usp=sharing'
    }
    csv_path = os.path.join(os.path.dirname(__file__), 'QuestionProfiles.csv')
    with open(csv_path) as file:
        reader = csv.reader(file)
        num_classes = 0
        for line in reader:
            num_classes = max(len(line), num_classes)
        num_classes -= 2
        file.seek(0)
        classes = [0 for _ in range(num_classes)]
        for row in reader:
            if row[0]:
                current = row[0]
            if row[1] == answers[current]:
                for i in range(num_classes):
                    classes[i] += float(row[2+i])
    profile = str(classes.index(max(classes)) + 1)
    return links[profile]

def get_OSWENTRY_Questionnaire():
    csv_path = os.path.join(os.path.dirname(__file__), 'OSWESTRY_pain.csv')
    with open(csv_path) as file:
        reader = csv.reader(file)
        questions = [row for i, row in enumerate(reader) if i]
    return questions

def score_OSWENTRY(answers):
    questions = get_OSWENTRY_Questionnaire()
    question_length = len(questions)
    score = 0
    for i in range(question_length):
        answer = answers.get(f'{i + 1}')
        if answer is None:
            continue
        score += (questions[i].index(answer) - 2)
    return score

def get_disability_level_from_score(score):
    if score < 5:
        return 'No Disability'
    elif score < 15:
        return 'Mild Disability'
    elif score < 25:
        return 'Moderate Disability'
    elif score < 35:
        return 'Severe Disability'
    else:
        return 'Completely Disabled'
