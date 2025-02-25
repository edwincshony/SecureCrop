from django.shortcuts import render, get_object_or_404,redirect
from .models import Pest, Weed
from django.db.models import Q

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



