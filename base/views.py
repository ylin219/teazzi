from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Section,Drink,Topping, Chart
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    drink = Drink.objects.filter(
        Q(section__name__icontains = q) |
        Q(name__icontains = q) 
        )
    section = Section.objects.all()
    chart = Chart.objects.all()
    total_price = Chart.objects.all().aggregate(Sum('price'))['price__sum']
    if total_price == None:
        total_price=0
    return render(request,'base/home.html',{'section':section,'drink':drink,'chart':chart,'total_price':total_price})
# def items(request,pk):
#     return render(request,'base/items.html')
@login_required(login_url='login')
def topping(request,pk):
    topping = Topping.objects.all()
    drink = Drink.objects.get(id=pk)
    if request.method == 'POST':
        # topping_list = request.POST.get('ice')
        total = 0
        print(request.POST['sugar'])
        print(request.POST['ice'])
        print(request.POST.getlist('topping'))
        chartins = Chart.objects.create(
            drink = drink,
            user = request.user,
            sugar = request.POST['sugar'],
            ice = request.POST['ice'],
            price = 0
        )
        total+=drink.price
        for i in request.POST.getlist('topping'):
            topping_temp = Topping.objects.get(name=i)
            chartins.toppings.add(topping_temp)
            total+=topping_temp.price
        chartins.price += total
        chartins.save()
        return redirect('/')
    return render(request,'base/topping.html',{'topping':topping,'drink':drink})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username =username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request, 'base/login_register.html',{'form':form})

@login_required(login_url='login')
def deleteTopping(request,pk):
    chart = Chart.objects.get(id=pk)
    chart.delete()
    return redirect('home')

@login_required(login_url='login')
def likeDrinkt(request,pk):
    drink = Drink.objects.get(id=pk)
    drink.like+=1
    drink.save()
    return redirect('home')
