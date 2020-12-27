from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.http import HttpResponse
import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from datetime import datetime
from datetime import timedelta
import time
import json
from .models import Status
past_days = 1
matplotlib.use("Agg")


def index(request):
    global past_days
    now_unix = int(time.time())
    now_dt = datetime.fromtimestamp(now_unix)
    past_dt = now_dt - timedelta(days=past_days)
    past_unix = int(datetime.timestamp(past_dt))
    dataset = Status.objects.filter(timestamp__gt=past_unix)
    df = pd.DataFrame(list(dataset.values()))
    df['stamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['Current humidity'] = df['current_moisture']
    df['Target humidity'] = df['target_moisture']
    df.plot(x='stamp',
            y=['Current humidity', 'Target humidity'],
            xlabel='Time',
            ylabel='Humidity',)
    last = dataset.order_by('-id')[0]
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    state_json = {
        'timestamp': datetime.fromtimestamp(last.timestamp),
        'mode': last.mode,
        'relay_target_status': last.relay_target_status,
        'target_moisture': last.target_moisture,
        'current_moisture': last.current_moisture,
        'relay_current_state': last.relay_current_state,
        'past_days': past_days
    }
    return render(request, 'mainpage.html', {'data': image_base64, 'table': df, 'state': state_json})


def login(request):
    if request.method == 'POST':  # Sign in button is pushed
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
        user = authenticate(request, username=request.POST.get('email', None), password=request.POST.get('password', None))
        if user is not None:  # correct credentials
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else: # Wrong username or password
            context = {'error': 'Wrong credentials!', 'email': request.POST.get('username', None)}
            # Return an 'invalid login' error message.
            return auth_views.LoginView.as_view(template_name='login.html', extra_context=context)(request)
    else: # Get request -> load the page
        email = request.GET.get('email', None)
        if email is None:
            return render(request, 'login.html')
        else:
            return render(request, 'login.html', {'email': email})


def auto_on(request):
    if request.method == 'POST':
        url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/mode'
        body = {'mode': 'auto'}
        response = requests.post(url, json=body)
    #return redirect('/')
    return HttpResponse("Ok")


def auto_off(request):
    if request.method == 'POST':
        url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/mode'
        body = {'mode': 'manual'}
        response = requests.post(url, json=body)
    return HttpResponse("Ok")


def set_target_humidity(request):
    if request.method == 'POST':
        url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/target'
        body = request.body.decode('utf-8')
        body = json.loads(body)
        response = requests.post(url, json=body)
    return HttpResponse("Ok")


def irrigation_on(request):
    if request.method == 'POST':
        url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/relay'
        body = {'relay': 'on'}
        response = requests.post(url, json=body)
    return HttpResponse("Ok")


def irrigation_off(request):
    if request.method == 'POST':
        url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/relay'
        body = {'relay': 'off'}
        response = requests.post(url, json=body)
    return HttpResponse("Ok")


def past_days_view(request):
    global past_days
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        past_days = int(body['past_days'])
        if past_days <= 0:
            past_days = 1
    return HttpResponse("Ok")


def about(request):
    return render(request, 'about.html')

