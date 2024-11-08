from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url='logout-user')  # Redirects to the login page if not authenticated
def index(request):
    return render(request, 'index.html')

