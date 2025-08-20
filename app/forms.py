from django import forms
from .models import Case, Candidate

from django import forms

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'support_type',
            'candidate',
            'date',
            'start_time',
            'end_time',
            'company',
            'round',
            'expert',
            'task',
            'feedback',
            'candidate_technology',
            'candidate_email',
            'candidate_phone',
        ]
        widgets = {
            'support_type': forms.Select(attrs={'class': 'form-control'}),
            'candidate': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'company': forms.Select(attrs={'class': 'form-control'}),  # <-- changed
            'round': forms.Select(attrs={'class': 'form-control'}),
            'expert': forms.Select(attrs={'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
# render snapshot fields as read-only text inputs
            'candidate_technology': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'candidate_email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'candidate_phone': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        


    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        # Filter candidates to only those assigned to the expert profile of the logged-in user
        
        self.fields['candidate'].queryset = Candidate.objects.all()
    
from django import forms

class BusyTimeForm(forms.Form):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))


class CaseEditForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['task', 'round', 'feedback']  # only these can be changed
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'round': forms.Select(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }