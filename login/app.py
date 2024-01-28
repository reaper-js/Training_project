from flask import Flask, request, render_template
import random
import smtplib
import pyodbc
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

app = Flask(__name__)

# Database connection details
server = 'dbserver23jandeepak.database.windows.net'
database = 'dbfeedbackmgt'
username = 'dbadmin'
password = 'Localhost@1234567'
driver = '{SQL Server}'

# Connect to your database
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server +
                      ';PORT=1433;DATABASE=' + database +
                      ';UID=' + username + ';PWD=' + password)

# In-memory storage for OTPs, keyed by email
otp_storage = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp
    send_email(email, otp)
    return render_template('verify_otp.html', email=email)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    cursor = cnxn.cursor()
    email = request.form.get('email')
    otp = int(request.form.get('otp'))
    if otp_storage.get(email) == otp:
        cursor.execute("SELECT Name, Role FROM Users WHERE Email = ?", email)
        row = cursor.fetchone()
        if row:
            if row.Role.lower() == 'trainer':
                return render_template('Trainer.html', name=row.Name)
            elif row.Role.lower() == 'student':
                return render_template('Student.html', name=row.Name)
        else:
            return 'User not found'
    else:
        return 'Invalid OTP'


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')

    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Users (Email, Name) VALUES (?, ?)",
                   email, name)
    cnxn.commit()
    return f'Welcome, {name}'

def send_email(email, otp):
    sender_email = "deepak0021099@gmail.com"
    sender_password = "tbvk xzws bzrn ywqe"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your OTP"
    message["From"] = sender_email
    message["To"] = email

    html = f"<html><body><p>Your OTP is: <strong>{otp}</strong></p></body></html>"

    part = MIMEText(html, "html")
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

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

@app.route('/show_question')
def show_question():
    # Establish a database connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Fetch questions from the database
    cursor.execute('SELECT * FROM Question')
    questions = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Render the Student.html page with the fetched questions
    return render_template('Student.html', questions=questions)

'''
@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
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
    return render_template('Student.html', questions=[], message='Your answers have been submitted successfully!')
    '''

if __name__ == '__main__':
    app.run(debug=True)







