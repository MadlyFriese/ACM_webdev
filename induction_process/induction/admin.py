from django.contrib import admin
from django.shortcuts import render, redirect 
from django.urls import path
from .forms import ScheduleInterviewForm
from django.utils.html import format_html
from django.core.mail import send_mail
from .models import Applicant
from django.http import HttpResponseRedirect

ACTION_CHECKBOX_NAME = '_selected_action'

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'interview_time', 'feedback')
    list_filter = ('status', 'interview_time')
    search_fields = ('name', 'email')
    actions = ['schedule_interview', 'accept','reject', 'send_interview_email']




    
    def send_interview_email(self, request, queryset):
        
        for applicant in queryset:
            subject = 'Interview Scheduled'
            message = f'Dear {applicant.name},\n\nYour interview has been scheduled on {applicant.interview_time}.\n\nBest regards,\nClub'
            from_email = 'your-email@gmail.com'
            recipient_list = [applicant.email]
            send_mail(subject, message, from_email, recipient_list)

        
        self.message_user(request, "Interview emails have been sent to the selected applicants.")

    send_interview_email.short_description = "Send interview email to selected applicants"

    def get_urls(self):
        
        urls = super().get_urls()
        custom_urls = [
            path('schedule_interview/', self.admin_site.admin_view(self.schedule_interview_action), name='schedule_interview'),
        ]
        return custom_urls + urls

    
    def schedule_interview(self, request, queryset):
    
        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)  
        return HttpResponseRedirect(f'./schedule_interview/?ids={",".join(selected)}')

    schedule_interview.short_description = "Schedule interview for selected applicants"

    def schedule_interview_action(self, request):
        ids = request.GET.get('ids')
        applicants = Applicant.objects.filter(id__in=ids.split(','))

        if request.method == 'POST':
            form = ScheduleInterviewForm(request.POST)
            if form.is_valid():
                interview_time = form.cleaned_data['interview_time']
                for applicant in applicants:
                    applicant.interview_time = interview_time
                    applicant.status = 'interview_scheduled'
                    applicant.save()
                self.message_user(request, f"Interviews scheduled for {applicants.count()} applicants.")
                return redirect('admin:induction_applicant_changelist')
        else:
            form = ScheduleInterviewForm()

        context = {
            'form': form,
            'applicants': applicants,
            'title': f'Schedule Interview for {applicants.count()} applicants'
        }

        return render(request, 'admin/schedule_interview.html', context)

    def accept(self, request, queryset):
        queryset.update(status='accepted') 
        for applicant in queryset:
            subject = 'You have been accepted'
            message = f'Dear {applicant.name},\n\nYou have been inducted.\n\nBest regards,\nClub'
            from_email = 'your-email@gmail.com'
            recipient_list = [applicant.email]
            send_mail(subject, message, from_email, recipient_list) 
        self.message_user(request, "Selected applicants have been accepted and email has been sent.")

    accept.short_description = "Accept selected applicants"

    def reject(self, request, queryset):
        queryset.update(status='rejected')
        for applicant in queryset:
            subject = 'Rejection'
            message = f'Dear {applicant.name},\n\nYou have been rejected.\n\nBest regards,\nClub'
            from_email = 'your-email@gmail.com'
            recipient_list = [applicant.email]
            send_mail(subject, message, from_email, recipient_list)

        self.message_user(request, "Selected applicants have been rejected and email has been sent.")

    reject.short_description = "Reject selected applicants"

