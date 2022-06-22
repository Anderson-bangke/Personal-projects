
from celery import Celery
from time import sleep

from sqlalchemy import false, true

app = Celery('tasks', broker='amqp://localhost')

@app.task
def reverse(text):
    sleep(5)
    return text[::-1]

def checkPrime(num):
    j = 0
    if(num == 1) : return false
    else:
        for i in range(1, num):
            if(num % i == 0):
                j += 1
        if(j == 1): return true
        else : return false
            

@app.task
def prime_index(index):
    counter = 0
    num = 0
    while(index != counter):
        num += 1
        if (checkPrime(num) == true):
            counter += 1
    return num

@app.task
def prime_palindrom(index):
    counter = 0
    num = 0
    while(index != counter):
        num += 1
        if(checkPrime(num) == true):
            if(str(num) == str(num)[::-1]):
                counter += 1
    return num
            