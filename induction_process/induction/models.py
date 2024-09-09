from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('interview_scheduled', 'Interview Scheduled'),
    ('interview_completed', 'Interview Completed'),
    ('rejected', 'Rejected'),
    ('accepted', 'Accepted'),
]

class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    interview_time = models.DateTimeField(null=True, blank=True)
    interview_panel = models.ManyToManyField(User, blank=True)
    feedback = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name


