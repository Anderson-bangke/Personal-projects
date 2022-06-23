from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect

from .form import GenerateUserForm
from .task import create_random_user_accounts, prime_index, prime_palindrom

from django.http import HttpResponse
import datetime

#example
class UserListView(ListView):
    template_name = 'task/user_list.html'
    model = User
    
class GenerateRandomUserView(FormView):
    template_name = 'task/generate_user.html'
    form_class = GenerateUserForm
    
    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delat(total)
        messages.success(self.request, 'Method should be POST')
        return redirect('user_list')

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def prime(request, index):
    prime = prime_index(index= index)
    html = '<html><h1> Prime %s. </h1></html>'  %prime
    return HttpResponse(html)

def palindrome(request, n):
    palindrome = prime_palindrom(index= n)
    html = '<html><h1> Prime and Palindrome %s. </h1></html>' %palindrome
    return HttpResponse(html)

# Create your views here.
