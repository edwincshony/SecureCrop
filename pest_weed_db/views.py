from django.shortcuts import render, get_object_or_404,redirect
from .models import Pest, Weed
from itertools import groupby  # Add this import
from django.utils.decorators import method_decorator
from django.contrib import messages
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
    model = Weed
    success_url = reverse_lazy('weed_list')  # Changed to match named URL

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Crop
from agricultural_expert.forms import CropForm

# List View
def crop_list(request):
    query = request.GET.get('q', '')
    crops = Crop.objects.filter(
        Q(name__icontains=query) |
        Q(species__icontains=query) |
        Q(description__icontains=query)
    ).order_by('name')
    return render(request, 'crop_list.html', {'crops': crops, 'query': query})

# Detail View
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, 'crop_detail.html', {'crop': crop})

# Create View
class CropCreateView(LoginRequiredMixin, ExpertRequiredMixin, CreateView):
    model = Crop
    form_class = CropForm
    template_name = 'crop_form.html'
    success_url = reverse_lazy('crop_list')

class CropUpdateView(LoginRequiredMixin, ExpertRequiredMixin, UpdateView):
    model = Crop
    form_class = CropForm
    template_name = 'crop_form.html'
    success_url = reverse_lazy('crop_list')


@method_decorator(csrf_exempt, name='dispatch')
class CropDeleteView(LoginRequiredMixin, ExpertRequiredMixin, DeleteView):
    model = Crop
    success_url = reverse_lazy('crop_list')

    def delete(self, request, *args, **kwargs):
        crop = self.get_object()
        crop.delete()
        return JsonResponse({'success': True})

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import CropLifecycle
from .forms import CropLifecycleForm

class CropLifecycleListView(ListView):
    model = CropLifecycle
    template_name = 'crop_lifecycle/lifecycle_list.html'
    context_object_name = 'lifecycles'

    STAGE_ORDER = {
        'planting': 1,
        'watering': 2,
        'pest_treatment': 3,
        'advisory': 4,
        'fertilizer': 5,
        'sunlight': 6,
        'harvesting': 7,
        'post_harvest': 8,
    }

    def get_queryset(self):
            queryset = CropLifecycle.objects.filter(user=self.request.user).order_by('crop__name', '-date')
            crop_filter = self.request.GET.get('crop', '')
            if crop_filter:
                queryset = queryset.filter(crop__name=crop_filter)
            return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_lifecycles = {}

        sorted_lifecycles = sorted(
            self.get_queryset(),
            key=lambda x: (self.STAGE_ORDER.get(x.stage, 99), x.crop.name)
        )

        for (crop, stage), events in groupby(sorted_lifecycles, key=lambda x: (x.crop.name, x.stage)):
            grouped_lifecycles[(crop, stage)] = list(events)

        # Add available crops for the filter dropdown
        context['grouped_lifecycles'] = grouped_lifecycles
        context['available_crops'] = Crop.objects.values_list('name', flat=True).distinct()
        context['selected_crop'] = self.request.GET.get('crop', '')
        return context


class CropLifecycleCreateView(LoginRequiredMixin, CreateView):
    model = CropLifecycle
    form_class = CropLifecycleForm
    template_name = 'crop_lifecycle/lifecycle_form.html'
    success_url = reverse_lazy('crop_lifecycle_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CropLifecycleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CropLifecycle
    form_class = CropLifecycleForm
    template_name = 'crop_lifecycle/lifecycle_form.html'
    success_url = reverse_lazy('crop_lifecycle_list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.user or self.request.user.role in ['farmer', 'agricultural_expert'] or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this milestone.")
        return redirect('crop_lifecycle_list')


from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import CropLifecycle

class CropLifecycleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CropLifecycle
    success_url = reverse_lazy('crop_lifecycle_list')

    def test_func(self):
        event = self.get_object()
        return (
            self.request.user == event.user or
            self.request.user.role in ['farmer', 'agricultural_expert'] or
            self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(self.request, "Permission denied!")
        return redirect(self.success_url)