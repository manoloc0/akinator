import csv
from pathlib import Path

def update_char(char_name, questions, answers):
    global times_played
    # Read data
    path = Path(__file__).parent.resolve() / "characters.csv"

    with path.open() as f:
        reader = csv.reader(f)
        rows = list(reader)



    # Update data
    for row in rows:
        if row[0] == char_name:
            # Check if the current value is a non-empty string before conversion
            if row[1].strip():
                times_played = int(row[1]) + 1
                row[1] = str(times_played)
            else:
                times_played = 1
                row[1] = str(times_played)
            #Iterate through all of the questions. The same index on answers array has the answer. Update the entire row with it.
            for i in range(len(questions)):
                idx = questions[i] + 1
                print(idx)
                old_avg = float(row[idx])
                ans = float(answers[i])
                if (old_avg < 1):       # If this questions has never been asked, update the csv with the answer
                    row[idx] = ans
                else:
                    new_avg = (old_avg * (times_played-1) + ans)/times_played       #Otherwise, update the average
                    row[idx] = new_avg

    # Write updated data back to CSV
    with path.open(mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return times_played

def augment_chars(char_name, questions, answers):
    # Read data

    path = Path(__file__).parent.resolve() / "characters.csv"

    with path.open() as f:
        reader = csv.reader(f)
        rows = list(reader)


    # Assuming questions contains the column indices for the new row
    new_row = [char_name] + [0] + [0.5] * (len(rows[0])-2)

    # Update the values in the new row based on the provided answers
    for i, question_idx in enumerate(questions):
        new_row[question_idx+1] = float(answers[i])

    # Append the new row to the list of rows
    rows.append(new_row)

    # Write the updated data back to the CSV file
    with path.open(mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)





