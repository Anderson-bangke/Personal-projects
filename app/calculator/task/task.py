import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from sqlalchemy import false, true

def checkPrime(num):
    j = 0
    if(num == 1) : return false
    else:
        for i in range(1, num):
            if(num % i == 0):
                j += 1
        if(j == 1): return true
        else : return false
        
#template task
@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format (total)

#calculator task
@shared_task
def prime_index(index):
    counter = 0
    num = 0
    while(index != counter):
        num += 1
        if (checkPrime(num) == true):
            counter += 1
            
    return num

@shared_task
def prime_palindrom(index):
    counter = 0
    num = 0
    while(index != counter):
        num += 1
        if(checkPrime(num) == true):
            if(str(num) == str(num)[::-1]):
                counter += 1
                
    return num