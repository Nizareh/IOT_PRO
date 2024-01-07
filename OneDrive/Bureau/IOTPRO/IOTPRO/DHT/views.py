from django.shortcuts import render, get_object_or_404, redirect
from .models import Dht11
from django.utils import timezone
from datetime import timedelta
import csv
from django.http import HttpResponse, JsonResponse
from datetime import timedelta, datetime
import telepot
from .models import Member
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm



def index(request):
    latest_dht11_object = Dht11.objects.last()
    if latest_dht11_object:
        derniere_date = latest_dht11_object.dt
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60
        temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
        if difference_minutes > 60:
            temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
        valeurs = {'date': temps_ecoule, 'id': latest_dht11_object.id, 'temp': latest_dht11_object.temp, 'hum': latest_dht11_object.hum}
    else:
        valeurs = {'date': 'N/A', 'id': 'N/A', 'temp': 'N/A', 'hum': 'N/A'}
    return render(request, 'pages/index.html', {'valeurs': valeurs})

def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response

def index_view(request):
    return render(request, 'index.html')

def graphique(request):
    return render(request, 'Chart.html')
def chart_data(request):
    dht = Dht11.objects.all()
    data = {
        'temps': [entry.dt for entry in dht],
        'temperature': [entry.temp for entry in dht],
        'humidity': [entry.hum for entry in dht]
    }
    return JsonResponse(data)

def chart_data_jour(request):
    now = timezone.now()
    last_24_hours = now - timezone.timedelta(hours=24)
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [entry.dt for entry in dht],
        'temperature': [entry.temp for entry in dht],
        'humidity': [entry.hum for entry in dht]
    }
    return JsonResponse(data)

def chart_data_semaine(request):
    date_debut_semaine = timezone.now().date() - timedelta(days=7)
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)
    data = {
        'temps': [entry.dt for entry in dht],
        'temperature': [entry.temp for entry in dht],
        'humidity': [entry.hum for entry in dht]
    }
    return JsonResponse(data)
def chart_data_mois(request):
    date_debut_mois = timezone.now().date() - timedelta(days=30)
    dht = Dht11.objects.filter(dt__gte=date_debut_mois)
    data = {
        'temps': [entry.dt for entry in dht],
        'temperature': [entry.temp for entry in dht],
        'humidity': [entry.hum for entry in dht]
    }
    return JsonResponse(data)

def sendtele():
    token = '6610739160:AAHOAHvDKA0cIZhyCTqiFQ5gxUuJ8-fuSQ8'
    rece_id = 5094847885
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))

def tables(request):
    mem=Member.objects.all()
    return render(request,'DHT/tables.html',{'mem':mem})

def add(request):
    return render(request,'DHT/add.html')

def addrec(request):
    x=request.POST['first']
    y=request.POST['last']
    z=request.POST['country']
    mem=Member(firstname=x,lastname=y,country=z)
    mem.save()
    return redirect("tables")

def delete(request,id):
    mem=Member.objects.get(id=id)
    mem.delete()
    return redirect("tables")

def update(request,id):
    mem=Member.objects.get(id=id)
    return render(request,'DHT/update.html',{'mem':mem})

def uprec(request,id):
    x=request.POST['first']
    y=request.POST['last']
    z=request.POST['country']
    mem=Member.objects.get(id=id)
    mem.firstname=x
    mem.lastname=y
    mem.country=z
    mem.save()
    return redirect("tables")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Rediriger vers la page du tableau de bord après la connexion
    else:
        form = LoginForm()

    return render(request, 'pages/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Rediriger vers la page du tableau de bord après l'inscription
    else:
        form = RegisterForm()

    return render(request, 'pages/register.html', {'form': form})
