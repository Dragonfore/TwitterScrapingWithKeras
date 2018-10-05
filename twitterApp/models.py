import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class evaluation(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    ym = models.FloatField(max_length=10)
    homogeneity = models.FloatField(max_length=10)
    plowing = models.FloatField(max_length=10)
    biological = models.FloatField(max_length=10)
    chemical = models.FloatField(max_length=10)
    hardness = models.FloatField(max_length=10)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text