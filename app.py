#Learner DAsboard

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbserver23jandeepak.database.windows.net;DATABASE=dbfeedbackmgt;UID=dbadmin;PWD=Localhost@1234567')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Question')
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', questions=questions, message=None)

@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    conn = get_db_connection()
    cursor = conn.cursor()
    for key, value in request.form.items():
        if key.startswith('answer_'):
            question_id = key.split('_')[1]  # Extract question_id from the key
            given_answer = value.strip()
            cursor.execute('SELECT correct_answer FROM Question WHERE question_id = ?', (question_id,))
            correct_answer = cursor.fetchone()[0]
            cursor.execute("INSERT INTO Answer (student_id, question_id, given_answer, correct_answer) VALUES (?, ?, ?, ?)", (None, question_id, given_answer, correct_answer))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('index.html', questions=[], message='Your answers have been submitted successfully!')

if __name__ == '__main__':
    app.run(debug=True)