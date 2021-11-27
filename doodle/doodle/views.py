from django.http.response import JsonResponse
from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chats.models import Room, ChatMessage, Score
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import os
import random
import json

def main_view_0(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, room_code = room_id, room_type = "public", current_player = user)
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_1(request):
    user = request.user
    room_id = generateRoomCode()
    if user.is_authenticated:
        Room.objects.create(owner = user, room_code = room_id, room_type = "private", current_player = user)
        return redirect(f'/lobby/{room_id}')
    else:
        return redirect('/accounts/login')

def main_view_2(request, room_id):
    user = request.user
    if user.is_authenticated:
        if exist(room_id):
            template = loader.get_template('main.html')
            room = Room.objects.get(room_code=room_id)
            
            if user not in room.rem_players.all() and user not in room.done_players.all():
                user.user_score.score = 0
                room.rem_players.add(user)
                user.user_score.save()

            chat_messages = room.messages.all().order_by('-timestamp')
            canvas_url = room.canvas_data_url 
            context = {
                'room': room, 
                'chat_messages': chat_messages,
                'canvas_url': canvas_url,
                'loggedin': user,
                'curr': room.current_player,
                'start': json.dumps(room.startTime.isoformat()),
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
        admin = []
        nonadmin = [] 
        for player in user_list:
            if player.is_superuser:
                admin.append(player)
            else :
                nonadmin.append((player, player.user_score.high_score))

        nonadmin.sort(reverse=True, key = lambda x: x[1])
        context = {
            'username': user.username,
            'admin': admin,
            'codelist': code_list,
            'loggedin': user,
            'nonadmin': nonadmin,
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
    data = {
        'guess' : False
    } 
    if request.method=='POST':
        message = request.POST.get('message')
        roomCode = request.POST.get('roomCode')
        author = request.POST.get('username')

        room = Room.objects.get(room_code=roomCode)
        user = User.objects.get(username=author)

        if user not in room.guessed.all():
            if message == room.word:
                user.user_score.score += int(60 - (timezone.now() - room.startTime).total_seconds())
                print(user.user_score.score)
                user.user_score.save()
                room.guessed.add(user)
                data['guess'] = True
            else:
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

def start_game(request):
    user = request.user
    if request.method=='POST':
        roomCode = request.POST.get('roomCode')
        room = Room.objects.get(room_code=roomCode)

        file_path = os.path.join(os.getcwd(), '../scraper/words.txt')
        room.word = random.choice(list(open(file_path)))[:-1].lower()
        room.round_no = 1
        room.current_player = room.rem_players.all()[0]
        room.guessed.add(room.current_player)
        room.started = True
        room.startTime = timezone.now()
        room.save()

        data = {}
        return JsonResponse(data)

def leave_room(request, room_id):
    user = request.user
    if user.is_authenticated:
        room = Room.objects.get(room_code=room_id)
        if user in room.rem_players.all():
            room.rem_players.remove(user)
        if user in room.done_players.all():
            room.done_players.remove(user)
        if user == room.current_player:
            update(room)
        # print(list(room.rem_players.all()))
        # print(list(room.done_players.all()))
        # if(len(room.rem_players.all()) + len(room.rem_players.all()) == 0):
        #     room.delete()
        return redirect('/menu')
    else:
        return redirect('/accounts/login')

def update_player(request):

    user = request.user
    if request.method=='POST':
        roomCode = request.POST.get('roomCode')
        room = Room.objects.get(room_code=roomCode)

        if((timezone.now() - room.startTime).total_seconds()<10):
            return {'bool' : False}

        if user == room.current_player:
            update(room)


    playerlist = {}

    for player in room.rem_players.all():
        playerlist[player.username] =  player.user_score.score

    for player in room.done_players.all():
        playerlist[player.username] =  player.user_score.score

    data = {
        'startTime' : room.startTime ,
        'currentPlayer' : room.current_player.username ,
        'word' : room.word ,
        'roundNo' : room.round_no ,
        'playerlist' : playerlist ,
        'bool' : True ,
        'started' : room.started
    }
    return JsonResponse(data)

def update(room):
    print('update')
    if room.current_player in room.rem_players.all():
        room.rem_players.remove(room.current_player)
        room.done_players.add(room.current_player)

    file_path = os.path.join(os.getcwd(), '../scraper/words.txt')
    room.word = random.choice(list(open(file_path)))[:-1].lower()
    room.guessed.through.objects.all().delete()
    room.canvas_data_url = 'none'

    if len(room.rem_players.all()) == 0:
        room.round_no += 1
        if room.round_no > 3:
            room.started = False
            for player in room.done_players.all():
                player.user_score.high_score = max(player.user_score.high_score, player.user_score.score)
                player.user_score.save()
            for player in room.rem_players.all():
                player.user_score.high_score = max(player.user_score.high_score, player.user_score.score)
                player.user_score.save()
        room.rem_players.add(*room.done_players.all())
        room.done_players.through.objects.all().delete()

    if len(room.rem_players.all()) == 0:
        room.current_player = room.owner
    else:
        room.current_player = room.rem_players.all()[0]
    room.guessed.add(room.current_player)
    room.startTime = timezone.now()
    room.save()

