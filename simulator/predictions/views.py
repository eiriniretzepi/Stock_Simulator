from django.shortcuts import render


def predictions(request):

    return render(request, 'predictions.html', {})

