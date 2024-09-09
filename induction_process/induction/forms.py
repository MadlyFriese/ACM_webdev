from django import forms
from .models import Applicant
from django.utils.timezone import now

class ScheduleInterviewForm(forms.Form):
    interview_time = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=now,
        label="Select Interview Time"
    )
class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(min_value=0, max_value=10)

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'phone']

class ApplicantEmailForm(forms.Form):
    email = forms.EmailField(max_length=100, label='Applicant Email', widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email address'
    }))
