from email import message
from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# room=[{'id':1,'name':'Python'},
#         {'id':2,'name':'Django'},
#         {'id':3,'name':'Js'}
# ]

# context={'room':room}

    
def LoginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('name')
        password=request.POST.get('password')
        print('Username',username)
        print('Password',password)
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user=authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context={'page':page}
    return render(request,'app/login_registration.html',context)

def LogoutPage(request):
    logout(request)

    return redirect('home')

def registerPage(request):
    page='register'
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            print('Inside VAlid')
            user=form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'app/login_registration.html',{'form':form})

def Home(request):
    q=request.GET.get('q','')
    room=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    topics=Topic.objects.all()
    room_count=room.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    print('------------------------DATA---------------------------------',room)
    return render(request,'app/Home.html',{'room':room,'topics':topics,'room_count':room_count,'room_messages':room_messages})

def Rooms(request,pk):
    data=Room.objects.get(id=pk)
    room_messages=Message.objects.filter(room=data)
    participants=data.participants.all()
    print(room_messages)
    print('data',data)

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=data,
            body=request.POST.get('body')
        )
        data.participants.add(request.user)
        return redirect('room',pk=data.id)

    context={'room':data,'room_messages':room_messages,'participants':participants}
    return render(request,'app/Room.html',context)

def userProfile(request):
    return render(request,'app/profile.html')

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(request,'app/room_form.html',context)

@login_required(login_url='login')
def updateMessage(request,pk):
    message=Message.objects.get(id=pk)
    formmessage=message.body
    if request.method=='POST':
        message.body=request.POST.get('message')
        message.save()
        return redirect('home')
    return render(request,'app/update-message.html',{'formmessage':formmessage})

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user!= room.host:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'app/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!= room.host:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'app/delete.html',{'room':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!= message.user:
        return HttpResponse('You are not allowed Here!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'app/delete.html',{'room':message})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    room=user.room_set.all()
    messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'room':room,'room_messages':messages,'topics':topics}
    return render(request,'app/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'app/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'app/topicsPage.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'app/activity.html', {'room_messages': room_messages})
