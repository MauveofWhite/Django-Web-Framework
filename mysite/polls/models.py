import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
"""
A model is the single, definitive source of truth about your data.

It contains the essential fields and behaviors of the data you’re storing.

Django follows the DRY (Don't Repeat Yourself) Principle.
    - Every distinct concept and/or piece of data should live in one, and only one, place.
The goal is to define your data model in one place and automatically derive things from it.
"""

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # <Question: Question object (1)> isn’t a helpful representation of this object
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # Old logic: if the quesiton was published within the last day, it's published recently.
        # However, it will also be true when asking a question that will be posted in the future,
        # which is false (the question hasn't been posted yet).
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        # Fixed:
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 

class Choice(models.Model):
    # ForeignKey tells Django that each Choice is related to a single Question.
    # A many-to-one relationship.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # <Question: Question object (1)> isn’t a helpful representation of this object
    def __str__(self):
        return self.choice_text
