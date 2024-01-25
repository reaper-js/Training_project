# quiz_app/views.py
from django.shortcuts import render, redirect
from .models import Question, Answer
from .forms import AnswerForm
# from .utils import send_email_to_client

#new updates
# from django.http import JsonResponse
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils.crypto import get_random_string
# from django.contrib.sessions.models import Session
#new updates end
def create_question(request):
    if request.method == 'POST':
        question_text = request.POST['question_text']
        Question.objects.create(text=question_text)
        return redirect('teacher_dashboard')
    return render(request, 'create_question.html')

def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('student_dashboard')
    else:
        form = AnswerForm()
    return render(request, 'answer_question.html', {'form': form, 'question': question})

def teacher_dashboard(request):
    questions = Question.objects.all()
    return render(request, 'teacher_dashboard.html', {'questions': questions})
                  
def home(request):
    return render(request, 'index.html')

#new updates
# def send_email(request):
#     send_email_to_client()
#     return redirect('/')
#newupdates end
#new updates
# def send_otp(request):
#     if request.method == 'POST':
#         user_type = request.POST.get('userType')
#         email = request.POST.get('email')

#         # Generate and save OTP in the session
#         otp = get_random_string(length=6, allowed_chars='1234567890')
#         request.session['otp'] = otp

#         # Send OTP via email
#         subject = 'Your OTP for authentication'
#         message = f'Your OTP is: {otp}'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [email]

#         try:
#             send_mail(subject, message, from_email, recipient_list)
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def verify_otp(request):
#     if request.method == 'POST':
#         user_otp = request.POST.get('otp')
#         saved_otp = request.session.get('otp')

#         if user_otp == saved_otp:
#             # OTP is valid, you can proceed with authentication
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'error': 'Invalid OTP'})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})
#newupdates end