from flask import Flask, render_template, request, send_file
import csv
from io import StringIO

app = Flask(__name__)

# Storage for inputs
questions_and_answers = []


@app.route('/', methods=['GET', 'POST'])
def index():
    global questions_and_answers

    if request.method == 'POST':
        asker_input = request.form['asker_input']
        thinker_input = request.form['thinker_input']
        questions_and_answers.append((asker_input, thinker_input))

        if 'done' in request.form or len(questions_and_answers) == 20:
            csv_data = generate_csv()
            save_to_csv(csv_data)
            return render_template('result.html', questions_and_answers=questions_and_answers,
                                   total_questions=len(questions_and_answers))

    elif request.method == 'GET':
        # If it's a GET request (start over), reset everything
        questions_and_answers = []

    return render_template('index.html', question_counter=len(questions_and_answers))


@app.route('/download_csv')
def download_csv():
    return send_file('game_result.csv', as_attachment=True, download_name='game_result.csv', mimetype='text/csv')


def generate_csv():
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Question', 'Reply'])
    csv_writer.writerows(questions_and_answers)
    output.seek(0)
    return output.getvalue()


def save_to_csv(csv_data):
    with open('game_result.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(csv_data)


if __name__ == '__main__':
    app.run(debug=True)
