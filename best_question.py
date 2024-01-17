import copy
import math

from basic_helpers import calculate_character_probability

global hypothetical_questions, hypothetical_answers

def find_best_question(questions_left, characters, questions_so_far, answers_so_far):
    # Initialization
    entropies = []
    global hypothetical_questions, hypothetical_answers
    hypothetical_questions = copy.deepcopy(questions_so_far)
    hypothetical_answers = copy.deepcopy(answers_so_far)

    print(hypothetical_questions)
    print(hypothetical_answers)
    print("hypothetical questions : " + str(type(hypothetical_questions)))
    print("questions " + str(questions_left))

    #Iterate through remaining questions
    for question in questions_left:
        #print("question" + str(question))
        # Calculate "yes" portion of minimum entropy equation
        character_entropy_given_yes, question_probability_given_yes = calculate_ans_entropy(characters, question, 1.0)
        character_entropy_given_no, question_probability_given_no = calculate_ans_entropy(characters, question, 0.0)
        entropies.append({'question': question, 'entropy': character_entropy_given_yes* question_probability_given_yes + character_entropy_given_no* question_probability_given_no})

    entropies = sorted(entropies, key=lambda p: p['entropy'], reverse=True)
    print("entropies: " + str(entropies))
    best_question = int(entropies[0]['question'])
    best_q_entropy = entropies[0]['entropy']
    print(best_question)
    return best_question, best_q_entropy

def calculate_ans_entropy(characters, question, ans):
    global hypothetical_questions, hypothetical_answers

    hypothetical_questions.append(question)
    hypothetical_answers.append(ans)
    total_character_entropy_given_ans = 0.0
    question_probability_given_ans = 0.0

    for character in characters:
        character_probability = calculate_character_probability(characters, character, hypothetical_questions, hypothetical_answers)
        total_character_entropy_given_ans += calculate_character_entropy(character_probability)
        question_probability_given_ans += calculate_question_probability_given_ans(character, question, character_probability)

    hypothetical_questions.pop()
    hypothetical_answers.pop()

    return(total_character_entropy_given_ans, question_probability_given_ans)

def calculate_character_entropy(character_probability):
    return character_probability * math.log2(1/ character_probability)

def calculate_question_probability_given_ans(character, question, char_prob):
    #print("Test answer array for char " + str(character.get('name')) + ": " + str(character['answers']))
    ans_prob = character['answers'][question]
    return char_prob * ans_prob





