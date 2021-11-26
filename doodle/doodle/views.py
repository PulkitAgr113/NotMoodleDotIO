from django.http.response import JsonResponse
from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chats.models import Room, ChatMessage, Score
from django.template import loader
from django.http import HttpResponse, JsonResponse
import os
import random

def main_view_0(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, room_code = room_id, room_type = "public")
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_1(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, room_code = room_id, room_type = "private")
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def change_timer(room_id):
    room = Room.objects.get(room_code=room_id)
    if room.started:
        room.timer -= 1
        if room.timer <= 0:
            room.timer = 60

def main_view_2(request, room_id):
    user = request.user
    if user.is_authenticated:
        if exist(room_id):
            template = loader.get_template('main.html')
            room = Room.objects.get(room_code=room_id)
            room.players.add(user)
            chat_messages = room.messages.all().order_by('-timestamp')
            canvas_url = room.canvas_data_url 
            context = {
                'roomid': room_id,
                'room': room, 
                'chat_messages': chat_messages,
                'canvas_url': canvas_url,
                'username': user.username,
                'loggedin': user,
                'curr': room.players.all()[room.current_player],
            }
            return HttpResponse(template.render(context, request))
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

    return JsonResponse(data)

def start_game(request, room_id):
    user = request.user
    if user.is_authenticated:
        room = Room.objects.get(room_code=room_id)
        if room.owner == user and (not room.started):
            room.started = True
            file_path = os.path.join(os.getcwd(), '../scraper/words.txt')
            room.word = random.choice(list(open(file_path)))
            room.save()
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def leave_room(request, room_id):
    user = request.user
    if user.is_authenticated:
        room = Room.objects.get(room_code=room_id)
        room.players.remove(user)
        return redirect('/menu')
    else:
        return redirect('/accounts/login')
