from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.
def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def index(request):

    return render(request, "dojosecrets/index.html")

def secrets(request):
    if 'user_id' in request.session:
        current_user = User.objects.currentUser(request)
        friends = current_user.friends.all()
        users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)
        context = {
            'users': users,
            'friends': friends,
        }
        return render(request,'dojosecrets/secrets.html', context)

    return redirect(reverse('landning'))

def register(request):
    if request.method == "POST":
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)

            request.session['user_id'] = user.id

            return redirect(reverse('secrets_app'))
        # for error in errors:
        #     # message.error(request, error)
        errors.append("Invaid account information")
    flashErrors(request, errors)

    return redirect(reverse('landing'))

def login(request):
    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()
            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)

                if hashed_pw == user.password:
                    request.session['user_id'] = user.id

                    return redirect(reverse('secrets_app'))

            errors.append("Invaid account information")
        flashErrors(request, errors)
    return redirect(reverse('landing'))

def logout(request):
    if 'user_id'in request.session:
        request.session.pop('user_id')
    return redirect(reverse('landing'))

def addFriend(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            current_user = currentUser(request)
            friend = User.objects.get(id=id)
            current_user.friends.add(friend)
            return redirect(reverse('secrets_app'))
    return redirect(reverse('landing'))

def removeFriend(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            current_user = User.objects.currentUser(request)
            friend = User.objects.get(id=id)
            current_user.friends.remove(friend)
            return redirect(reverse('secrets_app'))
    return redirect(reverse('landning'))
