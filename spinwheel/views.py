from django.shortcuts import render

def spin_wheel(request):
    return render(request, 'spinwheel/index.html')
