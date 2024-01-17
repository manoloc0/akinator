# Parse CSV
import csv
from pathlib import Path

def parse_csv():
    characters_list = []

    path = Path(__file__).parent.resolve() / "characters.csv"

    with path.open() as f:
        reader = csv.reader(f)
        for row in reader:
            characters_list.append(row)
        f.close()


    """with open('characters.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)"""


    questions = {}
    characters = []
    num_rows = len(characters_list)
    num_columns = len(characters_list[0])

    # Parse characters
    # Iterate through every row (and skip the title row)
    for i in range(num_rows - 1):
        answer_dict = {}
        characters_name = characters_list[i+1][0]

        #Create the dict of question ID's and answers
        for j in range(num_columns - 1):
            if (characters_list[i+1][j+1] == ''):        # Skips empty character amswer values
                continue
            if (float(characters_list[i + 1][j + 1]) < 0): # For now, just skip this
                answer_dict.update(
                {int(j): .5})  # Update the answer dict with what you just added
                continue
            answer_dict.update({int(j): float(characters_list[i+1][j+1])}) # Update the answer dict with what you just added

        character_data = {'name': characters_name, 'answers': answer_dict}
        characters.append(character_data)

    for i in range(num_columns - 2):
        questions.update({int(i+1): str(characters_list[0][i + 2])})

    print(characters)
    print(questions)
    return(characters, questions)