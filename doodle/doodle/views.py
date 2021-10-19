from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chats.models import Code
from django.template import loader
from django.http import HttpResponse
import random 

def main_view_0(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Code.objects.create(owner = user, owner_username = user.username, room_code = room_id, room_type = "public")
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_1(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Code.objects.create(owner = user, owner_username = user.username, room_code = room_id, room_type = "private")
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_2(request, room_id):
    user = request.user
    if user.is_authenticated:
        if exist(room_id):
            return render(request, 'main.html', {'username':user.username, 'roomid':room_id})
        else:
            return redirect('/menu')
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

def delete(request, room_id):
    user = request.user
    if user.is_authenticated:
        Code.objects.get(room_code = room_id).delete()
        return redirect('/menu')
    else:
        return redirect('/accounts/login')

def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/menu')
    else:
        return redirect('/accounts/login')

def menu(request):
    user = request.user
    if user.is_authenticated:
        template = loader.get_template('menu.html')
        user_list = User.objects.all()
        code_list = Code.objects.all()
        context = {
            'username': user.username,
            'userlist': user_list,
            'codelist': code_list,
            'loggedin': user,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/accounts/login')

def generateRoomCode():
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = '' 
    for i in range(6):
        code+= random.choice(str)
    return code

def exist(str):
    return Code.objects.filter(room_code = str).exists()