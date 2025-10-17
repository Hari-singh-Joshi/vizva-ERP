from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CaseForm
from .models import Case, Candidate,PH,Expert,Company
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Notification
from .forms import BusyTimeForm

from .forms import CaseEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Case, Candidate, Notification
# from .forms import BusyTimeForm  # ensure this is imported

@login_required
def case_list(request):
    # Handle BusyTimeForm submission
    if request.method == 'POST':
        form = BusyTimeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            message = f"{request.user.username} is busy from {start} to {end}."

            superusers = User.objects.filter(is_superuser=True)
            for superuser in superusers:
                Notification.objects.create(sender=request.user, recipient=superuser, message=message)

            messages.success(request, "Notification sent successfully.")
            return redirect('case-list')
    else:
        form = BusyTimeForm()

    # Only cases assigned/tagged to the logged-in expert
    expert_profile = getattr(request.user, 'expert_profile', None)  # <-- correct related_name
    if expert_profile:
        cases = (
            Case.objects
            .filter(expert=expert_profile, status__in=['assigned', 'tag'])
            .select_related('candidate', 'company', 'support_type', 'round', 'expert')
            .order_by('-date', '-start_time')
        )
    else:
        cases = Case.objects.none()

    # Optional filters
    date = request.GET.get('date')
    candidate = request.GET.get('candidate')
    company = request.GET.get('company')
    support_type = request.GET.get('support_type')

    if date:
        cases = cases.filter(date=date)
    if candidate:
        cases = cases.filter(candidate__name__icontains=candidate)
    if company:
        # company is a FK -> filter on its name field
        cases = cases.filter(company__company_name__icontains=company)
    if support_type:
        cases = cases.filter(support_type__support_name__icontains=support_type)

    candidates = Candidate.objects.all()

    return render(request, 'home.html', {
        'cases': cases,
        'candidates': candidates,
        'filter_date': date or "",
        'filter_candidate': candidate or "",
        'filter_company': company or "",
        'filter_support_type': support_type or "",
        'form': form,
    })



@login_required
def case_edit(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseEditForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            case.filled_by = request.user  
            case.save()
            messages.success(request, "Case updated successfully!")
            return redirect('case-list')
    else:
        form = CaseEditForm(instance=case)
    return render(request, 'case_form.html', {'form': form, 'edit': True, 'case': case})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('case-list')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('case-list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def po_entry_list(request):
    # Get the logged-in user's expert profile (if exists)
    try:
        expert_profile = request.user.expert_profile
    except Expert.DoesNotExist:
        expert_profile = None

    # Only show PO entries for candidates assigned to this expert
    if expert_profile:
        po_entries = PH.objects.filter(candidate__expert=expert_profile).order_by('-date')
    else:
        po_entries = PH.objects.none()  # No expert profile, show nothing

    # Filtering (optional, simple version)
    date = request.GET.get('date')
    candidate = request.GET.get('candidate')
    company = request.GET.get('company')

    if date:
        po_entries = po_entries.filter(date=date)
    if candidate:
        po_entries = po_entries.filter(candidate__name__icontains=candidate)
    if company:
        po_entries = po_entries.filter(company__icontains=company)

    return render(request, 'ph_list.html', {
        'ph_entries': po_entries,
        'filter_date': date or "",
        'filter_candidate': candidate or "",
        'filter_company': company or "",
    })

from django.shortcuts import render
from .models import Candidate

def candidate_list(request):
    expert = request.user.expert_profile  # assuming Expert is linked to User model (OneToOneField)
    candidates = Candidate.objects.filter(expert=expert, status_flag=True)
    return render(request, 'candidate.html', {'candidates': candidates})

