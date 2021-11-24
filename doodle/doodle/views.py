from django.http.response import JsonResponse
from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chats.models import Room
from chats.models import ChatMessage
from django.template import loader
from django.http import HttpResponse, JsonResponse
import random 

def main_view_0(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, owner_username = user.username, room_code = room_id, room_type = "public", canvas_data_url='none')
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_1(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, owner_username = user.username, room_code = room_id, room_type = "private", canvas_data_url='none')
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_2(request, room_id):
    user = request.user
    if user.is_authenticated:
        if exist(room_id):
            room = Room.objects.get(room_code=room_id)
            chat_messages = room.messages.all().order_by('-timestamp')
            canvas_url = room.canvas_data_url 
            return render(request, 'main.html', 
            {'username':user.username, 
            'roomid':room_id, 
            'chat_messages':chat_messages,
            'canvas_url':canvas_url},)
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
        Room.objects.get(room_code = room_id).delete()
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
        code_list = Room.objects.all()
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
    return Room.objects.filter(room_code = str).exists()

# Store message in database
def store_msg(request):
    data = {} 
    if request.method=='POST':
        message = request.POST.get('message')
        roomCode = request.POST.get('roomCode')
        author = request.POST.get('username')

        room = Room.objects.get(room_code=roomCode)

        ChatMessage.objects.create(room=room,text=message,author=author)
    return JsonResponse(data)

# Store canvas in database
def store_canvas(request):
    data = {}
    if request.method=='POST':
        canvas_url = request.POST.get('canvas_url')
        roomCode = request.POST.get('roomCode')

        room = Room.objects.get(room_code=roomCode)
        room.canvas_data_url = canvas_url
        room.save()
        print ('abc')

    return JsonResponse(data)