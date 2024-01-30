from flask import Flask,render_template,request,redirect,url_for,session
from flask_mail import Mail,Message
import os,random

app=Flask(__name__)
app.secret_key = '28janrandom'
app.secret_key = os.urandom(24)  

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465 #$587
app.config['MAIL_USERNAME'] = 'bbonzana@gmail.com'
app.config['MAIL_PASSWORD'] = 'eojchcxcrdozgnkb'
app.config['MAIL_USE_TLS'] = False #true
app.config['MAIL_USE_SSL'] = True #false
mail=Mail(app)

otp_storage=[11234,33243,43554,66765,76558,87575,64646,87876,12343,54366]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['emailname']
        otp = random.choice(otp_storage)
        session['otp'] = otp
        user_type = request.form['user_type']

        msg = Message("Your OTP", sender='bbonzana@gmail.com', recipients=[email])
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)

        return redirect(url_for('verify_otp', user_type = user_type))
    return render_template('index.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' in session:
        if request.method == 'POST':
            entered_otp = int(request.form['otpname'])
            stored_otp = session['otp']
            user_type = request.args.get('user_type')
            # print(user_type)
            if entered_otp == stored_otp:
                if user_type == 'learner':
                    return redirect(url_for('learner_dashboard'))
                elif user_type == 'trainer':
                    return redirect(url_for('trainer_dashboard'))
            else:
                return 'Invalid OTP. Please try again.'
        else:
            return render_template('verify_otp.html')
    else:
        return redirect(url_for('index'))

@app.route('/learner_dashboard')
def learner_dashboard():
    return render_template('learner_dashboard.html')

@app.route('/trainer_dashboard')
def trainer_dashboard():
    return render_template('trainer_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=80)




# def home():
#     if request.method=='POST':
#         if 'send_otp' in request.form:
#             email=request.form['emailname']
#             otp=random.choice(otp_storage)
#             session['otp']=otp

#             msg=Message("Your OTP",sender='bbonzana@gmail.com',
#                         recipients=[email])
#             msg.body=f"Your OTP is: {otp}"
#             mail.send(msg)
#             # return "sent email"
#             return render_template('verify_otp.html', email=email)
#         elif 'verify_otp' in request.form:
#             entered_otp = int(request.form['otpname'])
#             if 'otp' in session:
#                 stored_otp=session['otp']
#                 if entered_otp==stored_otp:
#                     return 'otp verified'
#                 else:
#                     return "invalid otp"
#             else:
#                 return 'otp session expired'
            
#     return render_template('index.html')




