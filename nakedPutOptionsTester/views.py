from django.shortcuts import render
from .forms import InputForm

def index(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "nakedPutOptionsTester/index.html", context)
