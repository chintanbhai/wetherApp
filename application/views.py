from django.shortcuts import render,redirect
from .forms import LoginForm,SignUpForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

# To use API 
import requests 

def get_weather_data(city):
    api_key = '2133091e2105982363f663eb160c6572'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius, 2)  

def weather(request):
    city = None
    temperature = None
    description = None

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            weather_data = get_weather_data(city)
            if weather_data['cod'] == 200:
                temperature_kelvin = weather_data['main']['temp']
                temperature = kelvin_to_celsius(temperature_kelvin)
                description = weather_data['weather'][0]['description']
            else:
                # Handle invalid city or API errors
                pass

    context = {
        'city': city,
        'temperature': temperature,
        'description': description,
    }
    return render(request, 'application/customer.html', context)




# Create your views here.
def index(request):
    return render(request,'application/index.html')

# def register(request):
#     return render(request,'application/signUp.html')
    
    
def register1(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'application/signUp.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'application/login.html', {'form': form, 'msg': msg})


def adminpage(request):
    return render(request,'application/adminpage.html')

@login_required(login_url='login')
def customer(request):
    return render(request,'application/customer.html')

@login_required(login_url='login')
def employee(request):
    return render(request,'application/employee.html')

@login_required(login_url='login')
def showSignup(request):
    return render(request,'application/auth_signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')