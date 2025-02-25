from django.shortcuts import render
from .forms import AdvisoryForm
from django.contrib.auth.decorators import login_required
from .models import AdvisoryRequest

@login_required
def advisory(request):
    if request.method == 'POST':
        form = AdvisoryForm(request.POST)
        if form.is_valid():
            advisory_request = form.save(commit=False)
            advisory_request.user = request.user
            advisory_request.status = 'pending'  # Default status
            advisory_request.save()
            return render(request, 'control_advisory/advisory_success.html', {'advisory_request': advisory_request})
    else:
        form = AdvisoryForm()
    
    return render(request, 'control_advisory/advisory_form.html', {'form': form})