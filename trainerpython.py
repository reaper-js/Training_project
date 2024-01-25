#Trainer-Dashboard
from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

# Database connection details
server = 'dbserver23jandeepak.database.windows.net'
database = 'dbfeedbackmgt'
username = 'dbadmin'
password = 'Localhost@1234567'
driver = '{SQL Server}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    question = request.form['question']
    shortcode = request.form['shortcode']
    question_type = request.form['question_type']
    correct_answer = None  # Initialize correct_answer with a default value
    mcq_options1 = None
    mcq_options2 = None
    mcq_options3 = None
    mcq_options4 = None

    # Determine the correct_answer based on the question type
    if question_type == 'yes_no':
        correct_answer = request.form['correct_answer']
    elif question_type == 'mcq':
        mcq_options1 = request.form['mcq_option_1']
        mcq_options2 = request.form['mcq_option_2']
        mcq_options3 = request.form['mcq_option_3']
        mcq_options4 = request.form['mcq_option_4']
        correct_answer = request.form['correct_answer']  
    elif question_type == 'descriptive' or question_type == 'text_answer':
        correct_answer = request.form['correct_answer'] 

    # Establish a database connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Insert the question data into the "Questions" table
    cursor.execute("INSERT INTO Question (question_text, shortcode, question_type, mcq_option_1, mcq_option_2, mcq_option_3, mcq_option_4, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   question, shortcode, question_type, mcq_options1, mcq_options2, mcq_options3, mcq_options4, correct_answer)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    return 'Question inserted into the database.'

@app.route('/show-answers', methods=['GET'])
def show_answers():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Answer')
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
