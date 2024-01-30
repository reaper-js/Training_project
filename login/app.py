from flask import Flask, request, render_template ,flash
import random
import smtplib
import pyodbc
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from flask_cors import CORS
from flask import jsonify   

app = Flask(__name__)
app.secret_key = 'e5c8b6c9c00e150734cd07ab14af9ee5'
CORS(app)
CORS(app, origins=["http://127.0.0.1:5000/"])  

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
stored_email = None

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
    global stored_email
    cursor = cnxn.cursor()
    email = request.form.get('email')
    otp = int(request.form.get('otp'))
    if otp_storage.get(email) == otp:
        cursor.execute("SELECT Name, Role FROM Users WHERE Email = ?", email)
        row = cursor.fetchone()
        if row:
            if row.Role.lower() == 'trainer':
                stored_email = email
                return render_template('Trainer.html', name=row.Name,email=email)
            elif row.Role.lower() == 'student':
                stored_email = email
                return render_template('Student.html', name=row.Name,email=email)
        else:
            stored_email = email
            return render_template('register.html',email=email)
    else:
        return 'Invalid OTP'


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    print(name)
    
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Users (Email, Name, Role) VALUES (?, ?, ?)",
                   (email, name, role))
    cnxn.commit()
    
    return render_template('Student.html', name=name, email=email)

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
    # return 'Question inserted into the database.'
    #flash('Question submitted successfully!', 'success')
    return render_template('Trainer.html', question_submitted=True)



@app.route('/add-another', methods=['GET'])
def add_another():
    return render_template('Trainer.html')

@app.route('/show-answers', methods=['GET'])
def show_answers():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Answer')
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('answer.html', answers=answers)

@app.route('/ask-question')
def index1():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbserver23jandeepak.database.windows.net;DATABASE=dbfeedbackmgt;UID=dbadmin;PWD=Localhost@1234567')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Question')
    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    questions_list = [
        {'id': row.question_id, 'text': row.question_text, 'type': row.question_type, 'options': [row.mcq_option_1,row.mcq_option_2,row.mcq_option_3,row.mcq_option_4]}
        for row in questions
    ]
    return jsonify(questions_list)

@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    conn = None
    try:
        # Establish a database connection
        global stored_email
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbserver23jandeepak.database.windows.net;DATABASE=dbfeedbackmgt;UID=dbadmin;PWD=Localhost@1234567')
        cursor = conn.cursor()

        # Retrieve data from the request
        data = request.get_json()
       
        print(stored_email)
        question_id = data.get('questionId')
        user_response = data.get('userResponse')
        
        # Processing the response based on its type
        if user_response in ["false", "true"]:
            user_response = "No" if user_response == "false" else "Yes"
        elif user_response in ["0", "1", "2", "3"]:
            option_column = f"mcq_option_{int(user_response) + 1}"
            cursor.execute(f'SELECT {option_column} FROM Question WHERE question_id = ?', question_id)
            user_response = cursor.fetchone()[0]

        # Get the correct answer from the database
        cursor.execute('SELECT correct_answer FROM Question WHERE question_id = ?', question_id)
        correct_answer = cursor.fetchone()[0]

        # Insert response into the Answer table with the email as student_id
        cursor.execute("INSERT INTO Answer (student_id, question_id, given_answer, correct_answer) VALUES (?, ?, ?, ?)", 
                       (stored_email, question_id, user_response, correct_answer))
        conn.commit()

        return jsonify({'status': 'success', 'message': 'Response submitted successfully'})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)







