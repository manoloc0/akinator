# Source code from Rogério Chaves, X account @_rchaves_

from flask import Flask, render_template, request, redirect, url_for, session
from best_question import find_best_question
# we will need those imports later
import random
from basic_helpers import calculate_probabilites, calculate_character_probability, character_answer
from update_csv import update_char, augment_chars
from parse_csv import parse_csv
0
# instantiate flask object
app = Flask(__name__)
app.secret_key = 'secret key'

global questions_so_far, answers_so_far, characters, questions
characters, questions = parse_csv()
questions_so_far = []
answers_so_far = []
global rounds, begin
rounds = 0
begin = False


@app.route('/', methods=['GET', 'POST']) #We must add 'POST' as allowable methods
def index():
    if request.method == 'GET':
        # Clear session data when accessing the index page
        session.clear()

    # Queue up guessable characters
    char_list = []
    for idx in range(len(characters) - 1):
        char_list.append(characters[idx + 1].get('name'))

    print("chars: " + str(char_list))

    if request.method == 'POST':    # If the method is a select box
        # Form submitted, check the action value
        action = request.form.get('action') #get the action associated from select box
        if action == 'begin':
            return redirect(url_for('pages'))
    return render_template('index.html', char_list = char_list)

@app.route('/pages', methods=['GET', 'POST'])
def pages():
    global result, rounds, begin
    global questions_so_far, answers_so_far, characters, questions

    if request.method == 'POST':    # If the method is a select box
        # Form submitted, check the action value
        action = request.form.get('action') #get the action associated from select box

        if action == 'play_again':
            return playagain()

        elif action == 'augment':
            print("user is augmenting")
            response_char = request.form.get('user_input')  # Assuming 'user_input' is the name attribute of your input field
            if not response_char.strip():
                playagain()
            augment_chars(response_char, questions_so_far, answers_so_far)
            return playagain()

        elif action == 'yes':
            print("User responded yes")
            response_char = result.get('name')
            times_played = update_char(response_char, questions_so_far, answers_so_far)
            correct_answer_message = "I win!"
            return render_template('pages.html', times_played = times_played, response_char= response_char, correct_answer_message=correct_answer_message)


        elif action == 'no':
            print("User responded no")
            response_char = result.get('name')
            rounds += 1
            if rounds >= 3:
                game_over_message = "I lose!"
                return render_template('pages.html', game_over_message = game_over_message)

            #Remove the incorrect answer from the dictionary
            for char in characters:
                if char.get('name') == response_char:
                    characters.remove(char)
                    break
            pass

    question = request.args.get('question')
    answer = request.args.get('answer')

    if question and answer:
        questions_so_far.append(int(question))
        answers_so_far.append(float(answer))

    probabilities = calculate_probabilites(characters, questions_so_far, answers_so_far)
    print("probabilities", probabilities)

    questions_left = list(set(questions.keys()) - set(questions_so_far))

    #If there are no qustions left
    if len(questions_left) == 0:
        result = sorted(probabilities, key=lambda p: p['probability'], reverse=True)[0]
        return render_template('pages.html', result=result['name'])

    #Set First Question
    if len(questions_so_far) == 0:
        next_question = 2
        print(sorted(probabilities, key=lambda p: p['probability'], reverse=True))
        return render_template('pages.html', question=next_question, question_text=questions[next_question])

    else:
        #Add condition here where if the entropy is low for even the best question, then probably stop. Perhaps stopping condition is for low entropy of best question and high probability of character.

        #next_question = random.choice(questions_left)
        #Working on this:
        next_question, best_q_entropy = find_best_question(questions_left, characters, questions_so_far, answers_so_far)

        #max_prob = float(max(probabilities, key=lambda x: x['probability'])['probability'])
        sorted_prob = sorted(probabilities, key=lambda p: p['probability'], reverse=True)
        max_prob = sorted_prob[0]['probability']
        contender_differential = sorted_prob[0]['probability'] - sorted_prob[1]['probability']
        print("max prob: " + str(max_prob))
        print("best_q_entropy" + str(best_q_entropy))
        print(sorted(
            probabilities, key=lambda p: p['probability'], reverse=True))

        # If the best question entropy is less than a certain threshold, end the game.
        if ((best_q_entropy < 3.0 ) & (max_prob > .90)) | (contender_differential > .15) | (best_q_entropy < 0.7): #| (max_prob > .1) NOTE: final conditional is for testing purposes only
            result = sorted(probabilities, key=lambda p: p['probability'], reverse=True)[0]
            return render_template('pages.html', result=result['name'])

        #print(next_question)
        #print(type(next_question))
        #print(questions[next_question])
        print(sorted(
            probabilities, key=lambda p: p['probability'], reverse=True))

        return render_template('pages.html', question=next_question, question_text=questions[next_question])

def playagain():
    global questions_so_far, answers_so_far, characters, questions, rounds
    print("PLaying again...")
    questions_so_far = []
    answers_so_far = []
    rounds = 0
    characters, questions = parse_csv()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8000)      #Changed to port 8000

