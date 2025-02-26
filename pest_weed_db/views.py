from django.shortcuts import render, get_object_or_404,redirect
from .models import Pest, Weed
from agricultural_expert.forms import PestForm, WeedForm
from django.views.generic import DeleteView
from agricultural_expert.views import ExpertRequiredMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy


def pest_list(request):
    query = request.GET.get('q', '')
    pests = Pest.objects.filter(
        Q(name__icontains=query) |
        Q(scientific_name__icontains=query) |
        Q(description__icontains=query)
    ).order_by('name')
    return render(request, 'pest_weed_db/pest_list.html', {'pests': pests, 'query': query})

def pest_detail(request, pk):
    pest = get_object_or_404(Pest, pk=pk)
    return render(request, 'pest_weed_db/pest_detail.html', {'pest': pest})

def weed_list(request):
    query = request.GET.get('q', '')
    weeds = Weed.objects.filter(
        Q(name__icontains=query) |
        Q(scientific_name__icontains=query) |
        Q(description__icontains=query)
    ).order_by('name')
    return render(request, 'pest_weed_db/weed_list.html', {'weeds': weeds, 'query': query})

def weed_detail(request, pk):
    weed = get_object_or_404(Weed, pk=pk)
    return render(request, 'pest_weed_db/weed_detail.html', {'weed': weed})

from django.urls import reverse_lazy

class PestCreateView(LoginRequiredMixin, ExpertRequiredMixin, CreateView):
    model = Pest
    form_class = PestForm
    template_name = 'pest_weed_db/pest_form.html'
    success_url = reverse_lazy('pest_list')  # Changed to match named URL

class PestUpdateView(LoginRequiredMixin, ExpertRequiredMixin, UpdateView):
    model = Pest
    form_class = PestForm
    template_name = 'pest_weed_db/pest_form.html'
    success_url = reverse_lazy('pest_list')  # Changed to match named URL

class WeedCreateView(LoginRequiredMixin, ExpertRequiredMixin, CreateView):
    model = Weed
    form_class = WeedForm
    template_name = 'pest_weed_db/weed_form.html'
    success_url = reverse_lazy('weed_list')  # Changed to match named URL

class WeedUpdateView(LoginRequiredMixin, ExpertRequiredMixin, UpdateView):
    model = Weed
    form_class = WeedForm
    template_name = 'pest_weed_db/weed_form.html'
    success_url = reverse_lazy('weed_list')  # Changed to match named URL

class PestDeleteView(LoginRequiredMixin, ExpertRequiredMixin, DeleteView):
    model = Pest
    success_url = reverse_lazy('pest_list')  # Changed to match named URL

class WeedDeleteView(LoginRequiredMixin, ExpertRequiredMixin, DeleteView):
    model = Pest
    success_url = reverse_lazy('pest_list')  # Changed to match named URL