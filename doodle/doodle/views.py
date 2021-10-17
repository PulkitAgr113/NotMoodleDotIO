from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
import random 

def main_view_1(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_2(request, room_id):
    user = request.user
    if user.is_authenticated:
        return render(request, 'main.html', {'username':user.username, 'roomid':room_id})
    else:
        return redirect('/accounts/login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
        else:
            return redirect('/accounts/login')
    else :
        form = RegistrationForm() 
        args = {'form':form}

        return render(request,'reg_form.html',args)


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/menu')
    else:
        return redirect('/accounts/login')

def menu(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'menu.html', {'username':user.username})
    else:
        return redirect('/accounts/login')

def generateRoomCode():
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = '' 
    for i in range(6):
        code+= random.choice(str)
    return code

    

