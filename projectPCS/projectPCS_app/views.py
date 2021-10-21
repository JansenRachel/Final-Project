from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime
# from django import template

# register = template.Library()

# @register.filter
# def days_until(date):
#     delta = datetime.date(request.POST['move_date']) - datetime.now().date()
#     return delta.days

# def remaining_days(self):
#     remaining = (datetime.now().date() - self.move_date.date()).days
#     return remaining

def day_counter():
    this_move = User.objects.get(id=request.session['user_id'])
    d0 = date(datetime.now())
    d1 = date(User.move_info.move_date)
    delta = d1=d0
    print(delta.days)


def index(request):
    return render(request, "login_reg.html")

def new_user(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create (firstname = request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password = pw_hashed)
        request.session['firstname'] = user.firstname
        request.session['lastname'] = user.lastname
        request.session['user_id'] = user.id
        request.session['email'] = user.email
        # return redirect("/home")
        return redirect("/myaccount_editprofile")
    
def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, "No record of that email, please register first")
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if user:
        logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        request.session['firstname'] = logged_user.firstname
        request.session['lastname'] = logged_user.lastname
        request.session['email'] = logged_user.email

        return redirect('/home')

def logout(request):
    request.session.flush()
    return redirect('/')

#   HOMEPAGE
def homepage(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "this_user" : User.objects.get(id=request.session['user_id'])
    }

#    TRYING TO GET DAYS LEFT COUNTER
    return render(request, "home.html", context)
    

#   MY ACCOUNT(ADD/UPDATE PCS INFO)
def add_pcs(request):
    move_info = Move_Info.objects.create(
    orig_address = request.POST['orig_address'],
    orig_citybase = request.POST['orig_citybase'],
    orig_state = request.POST['orig_state'],
    dest_address = request.POST['dest_address'],
    dest_citybase = request.POST['dest_citybase'],
    dest_state = request.POST['dest_state'],
    move_date = request.POST['move_date']
    )
    return redirect('/home')

def update_pcs(request, user_id):
    move = Move_Info.objects.get (id=user_id)
    move.orig_address = request.POST['orig_address']
    move.orig_citybase = request.POST['orig_citybase']
    move.orig_state = request.POST['orig_state']
    move.dest_address = request.POST['dest_address']
    move.dest_citybase = request.POST['dest_citybase']
    move.dest_state = request.POST['dest_state']
    move.move_date = request.POST['move_date']

#   TO-DO LIST
def toDo_list(request):
    return render(request, "toDo_list.html")
#   NEED TO KEEP CHECKBOXES CHECKED ON TO-DO LIST PAGE

#   MESSAGE BOARD
def message_board(request):

    one_user = User.objects.get(id=request.session['user_id'])

    context = {
        "user" : one_user,
        "all_messages" : Message.objects.all(),
        
    }
    return render(request, "message_board.html", context)

def new_post(request):
    if request.method == 'POST':
        errors = Message.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/messages')
        else:
            Message.objects.create(content = request.POST['postContent'], poster = User.objects.get(id=request.session['user_id']))
            return redirect('/messages')
    return redirect('/')


def delete_message(request, message_id):
    message_to_delete = Message.objects.get(id=message_id)
    message_to_delete.delete()
    return redirect('/messages')

def new_comment(request):
    if request.method == 'POST':
        Comment.objects.create(comment_content = request.POST['content'], poster = User.objects.get(id=request.session['user_id']), message = Message.objects.get(id=request.POST['message']))
        return redirect('/messages')
    return redirect('/')

#   MYACCOUNT
def uploads(request):
    return render(request, "uploads.html")

def editprofile(request):
    context = {
        "this_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "edit_account.html", context)

def update_profile(request, user_id):
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('update_profile/<int:user_id>')
    else:
        user = User.objects.get(id=user_id)
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.save()
    return redirect('/home')

