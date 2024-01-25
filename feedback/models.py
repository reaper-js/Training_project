
from django.db import models

class Question(models.Model):
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    answer = models.BooleanField()
