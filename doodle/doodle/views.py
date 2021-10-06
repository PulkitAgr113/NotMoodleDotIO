from django.shortcuts import redirect,render
from doodle.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm

def main_view(request):
    return render(request, 'main.html', {})

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
    return render(request, 'menu.html', {'username':user.username})

