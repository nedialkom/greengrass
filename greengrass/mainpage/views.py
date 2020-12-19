from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    url = 'https://3ovzkc5b71.execute-api.eu-central-1.amazonaws.com/production/greenhouse'
    data = {}
    data['days_ago'] = 1
    r = requests.get(url=url, params=data)
    data = r.json()
    df = pd.json_normalize(data)
    df['stamp'] = pd.to_datetime(df['timestamp'], unit='s')
    data = df.plot(x='stamp', y=['Payload.current moisture', 'Payload.target moisture'])

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return render(request, 'mainpage.html', {'data': image_base64})


def login(request):
    if request.method == 'POST':  # Sign in button is pushed
        if not request.POST.get('remember', None):
            request.session.set_expiry(0)
        user = authenticate(request, username=request.POST.get('email', None), password=request.POST.get('password', None))
        if user is not None: # correct credentials
            auth_login(request, user)
            return HttpResponseRedirect(reverse('base'))
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
