# Source code from Rogério Chaves, X account @_rchaves_

from flask import Flask, render_template, request
# we will need those imports later
import random, csv
import numpy as np

# instantiate flask object
app = Flask(__name__)

disorders_list = []
with open('6-disorders.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        disorders_list.append(row)
    csv_file.close()

# Parse CSV
questions = {}
characters = []
num_rows = len(disorders_list)
num_columns = len(disorders_list[0])

# Parse Disorders
# Iterate through every row (and skip the title row)
for i in range(num_rows - 1):
    answer_dict = {}
    disorder_name = disorders_list[i+1][0]

    #Create the dict of question ID's and answers
    for j in range(num_columns - 1):
        if(disorders_list[i+1][j+1] == ''):
            continue
        if (disorders_list[i + 1][j + 1][0] == '~'): # For now, just skip this
            continue
        answer_dict.update({int(j+1): float(disorders_list[i+1][j+1])})

    disorder_data = {'name': disorder_name, 'answers': answer_dict}
    characters.append(disorder_data)

for i in range(num_columns - 1):
    questions.update({int(i+1): 'What is the level of ' + str(disorders_list[0][i + 1]) + '?'})

print(characters)
print(questions)
print(type(characters))

# Create a new object that contains a dict with 'name' as the key and the name of the disorder as the value. The second object is a dict with 'answers' as the key and the value another dict. This dict has a value as the question ID and the value as the the value in the csv.

questions_so_far = []
answers_so_far = []

@app.route('/')
def index():
    global questions_so_far, answers_so_far

    question = request.args.get('question')
    answer = request.args.get('answer')
    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))

    probabilities = calculate_probabilites(questions_so_far, answers_so_far)
    print("probabilities", probabilities)

    questions_left = list(set(questions.keys()) - set(questions_so_far))
    if len(questions_left) == 0:
        result = sorted(
            probabilities, key=lambda p: p['probability'], reverse=True)[0]
        return render_template('index.html', result=result['name'])
    else:
        next_question = random.choice(questions_left)
        print(sorted(
            probabilities, key=lambda p: p['probability'], reverse=True))
        return render_template('index.html', question=next_question, question_text=questions[next_question])

def calculate_probabilites(questions_so_far, answers_so_far):
    probabilities = []
    for character in characters:
        probabilities.append({
            'name': character['name'],
            'probability': calculate_character_probability(character, questions_so_far, answers_so_far)
        })

    return probabilities

def calculate_character_probability(character, questions_so_far, answers_so_far):
    # Prior
    P_character = 1 / len(characters)

    # Likelihood
    P_answers_given_character = 1
    P_answers_given_not_character = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        P_answers_given_character *= max(
            1 - abs(answer - character_answer(character, question)), 0.01)

        P_answer_not_character = np.mean([1 - abs(answer - character_answer(not_character, question))
                                          for not_character in characters
                                          if not_character['name'] != character['name']])
        P_answers_given_not_character *= max(P_answer_not_character, 0.01)

    # Evidence
    P_answers = P_character * P_answers_given_character + \
        (1 - P_character) * P_answers_given_not_character

    # Bayes Theorem
    P_character_given_answers = (
        P_answers_given_character * P_character) / P_answers

    return P_character_given_answers

def character_answer(character, question):
    if question in character['answers']:
        return character['answers'][question]
    return 0.5

if __name__ == '__main__':
    app.run(port=8000)      #Changed to port 8000