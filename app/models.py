from django.db import models
from django.contrib.auth.models import User

class SupportType(models.Model):
    support_name = models.CharField(max_length=100)
    def __str__(self):
        return self.support_name

class Technology(models.Model):
    technology_name = models.CharField(max_length=100)
    def __str__(self):
        return self.technology_name
    
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    def __str__(self):
        return self.company_name    

class Round(models.Model):
    round_name = models.CharField(max_length=100)
    def __str__(self):
        return self.round_name

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    ]
    task_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    def __str__(self):
        return self.task_status
    
class MarketingTeam(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='marketing_profile',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    is_team_lead = models.BooleanField(default=False)
    date_of_joining = models.DateField(null=True, blank=True)
    team_lead = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='team_members'
    )
    status_flag = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Marketing Member"
        verbose_name_plural = "Marketing Team"

    def __str__(self):
        return self.name

   

class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile',null=True, blank=True)
    name = models.CharField(max_length=100)
    is_team_lead = models.BooleanField(default=False)
    date_of_joining = models.DateField(null=True, blank=True) 
    team_lead = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='team_members'
    )
    status_flag = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    technology = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name='candidates'
    )
    expert = models.ForeignKey(
        Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates'
    )
    recruiter = models.ForeignKey(
        MarketingTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates'
    )
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    resume=models.URLField(unique=True, help_text="Google Drive shareable link")
    status_flag = models.BooleanField(default=True)
    def __str__(self):
        return self.name

from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

class Case(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('tag', 'Tag'),
    ]
    support_type = models.ForeignKey(SupportType, on_delete=models.CASCADE, related_name='cases')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='cases')
    candidate_technology = models.CharField(max_length=100,null=True, blank=True)
    candidate_email = models.EmailField(max_length=255,null=True, blank=True)
    candidate_resume=models.URLField(unique=True,null=True, blank=True)
    candidate_phone = models.CharField(max_length=20,null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cases')
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='cases')
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    feedback = models.TextField(blank=True)
    JOB_DES = models.TextField(blank=True)
    filled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cases_filled')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tag')

    def clean(self):
        super().clean()
        # Require that the selected candidate has an assigned expert,
        # but DO NOT overwrite self.expert here (so manual change is allowed).
        if not self.candidate or not self.candidate.expert:
            raise ValidationError({'candidate': 'Selected candidate has no assigned expert.'})

    def save(self, *args, **kwargs):
        if kwargs.pop('validate', True):
            self.full_clean()

        # Snapshot candidate fields
        if self.candidate:
            self.candidate_technology = (
                self.candidate.technology.technology_name if self.candidate.technology else ''
            )
            self.candidate_email = self.candidate.email
            self.candidate_phone = self.candidate.phone_number
            self.candidate_resume=self.candidate.resume

        # Auto-fill expert only if user didn't choose one; otherwise keep manual choice
        if self.candidate and not self.expert:
            self.expert = self.candidate.expert

        # Status: 'assigned' if chosen expert equals candidate.expert, else 'tag'
        if self.candidate and self.expert:
            self.status = 'assigned' if self.candidate.expert_id == self.expert_id else 'tag'
        else:
            self.status = 'tag'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company} | {self.candidate.name} | {self.date} | Status: {self.get_status_display()}"

PO_TYPE_CHOICES = [
        ("INCENTIVIZED", 'Incentivized PO'),
        ("HONORABLE", 'Honorable PO'),
    ]
class PH(models.Model):
    date = models.DateField()
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name='ph_entries'
    )
    technology = models.ForeignKey(
        Technology, on_delete=models.CASCADE, related_name='ph_entries'
    )
    # CHANGED: CharField -> ForeignKey to Company
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ph_entries')
    expert = models.ForeignKey(
        Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='ph_entries'
    )
    team_lead = models.ForeignKey(
        Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_lead_ph_entries'
    )
    po_type = models.CharField(
        max_length=20,
        choices=PO_TYPE_CHOICES,
        default="INCENTIVIZED",
    )
    class Meta:
        verbose_name = "PO Entry"             # Singular name in admin
        verbose_name_plural = "PO Table"      # Plural name in admi
    def save(self, *args, **kwargs):
        # Auto-fill expert and team lead based on selected candidate and technology
        if self.candidate:
            # Prefer the candidate's assigned expert
            self.expert = self.candidate.expert
            # If expert exists, get their team lead
            if self.expert and self.expert.team_lead:
                self.team_lead = self.expert.team_lead
            else:
                self.team_lead = None
        super().save(*args, **kwargs)

    def __str__(self):
        expert_name = self.expert.name if self.expert else "N/A"
        team_lead_name = self.team_lead.name if self.team_lead else "N/A"
        return f"{self.company} | {self.candidate.name} | {self.date} | {expert_name} | {team_lead_name} | {self.po_type}"


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read = True
        self.save()

    def __str__(self):
        return f'Notification from {self.sender} to {self.recipient}: {self.message[:20]}'
    
