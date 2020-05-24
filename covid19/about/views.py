from django.shortcuts import render


def about(request):
    return render(request, 'about.html')


def description(request):
    return render(request, 'project_description.html')


def contact(request):
    return render(request, 'contact.html')
