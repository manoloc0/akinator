# Source code from Rogério Chaves, X account @_rchaves_

from flask import Flask, render_template, request
# we will need those imports later
import random
import numpy as np

# instantiate flask object
app = Flask(__name__)

disorders_list = []

questions = {
    1: 'Is your character yellow?',
    2: 'Is your character bald?',
    3: 'Is your character a man?',
    4: 'Is your character short?',
    5: 'Is your character chubby?'
}

characters = [
    {'name': 'Homer Simpson',         'answers': {1: 1, 2: 1, 3: 1, 4: 0, 5:1}},
    {'name': 'SpongeBob SquarePants', 'answers': {1: 1, 2: 1, 3: 1, 4: 0.75}},
    {'name': 'Sandy Cheeks',          'answers': {1: 0, 2: 0, 3: 0}},
    {'name': 'Patrick Star',          'answers': {1: 0, 2: 1, 3: 1, 4: .25, 5: 1}},
    {'name': 'Squidward',           'answers': {1: 0, 2: 1, 3: 1, 4: 0, 5: 0}},
    {'name': 'Ned Flanders',          'answers': {1: 1, 2: 0, 3: 1, 4: 0, 5: .5}}
]

print(characters)
print(type(characters))
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
    app.run(port=8080)      #Changed to port 8000