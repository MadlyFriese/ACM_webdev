from django.shortcuts import render, redirect
from .models import Applicant
from .models import Applicant
from .forms import ApplicantForm , ApplicantEmailForm



def applicant_dashboard(request):
    applicant = None
    status = None
    interview_time = None

    if request.method == 'POST':
        form = ApplicantEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                applicant = Applicant.objects.get(email=email)
                status = applicant.status
                interview_time = applicant.interview_time
            except Applicant.DoesNotExist:
                form.add_error('email', 'Applicant not found.')
    else:
        form = ApplicantEmailForm()

    return render(request, 'induction/applicant_dashboard.html', {
        'form': form,
        'applicant': applicant,
        'status': status,
        'interview_time': interview_time
    })



def create_applicant_profile(request):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.save()
            return redirect('applicant_dashboard')
    else:
        form = ApplicantForm()

    return render(request, 'induction/create_applicant_profile.html', {'form': form})


def home_page(request):
    return render(request,'induction/home.html')
