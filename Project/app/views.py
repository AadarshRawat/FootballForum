from multiprocessing import context
from django.shortcuts import render,HttpResponse
from .models import Room


# room=[{'id':1,'name':'Python'},
#         {'id':2,'name':'Django'},
#         {'id':3,'name':'Js'}
# ]

# context={'room':room}


def Home(request):
    data=Room.objects.all()
    print('------------------------DATA---------------------------------',data)
    return render(request,'app/Home.html',{'room':data})

def Rooms(request,pk):
    data=Room.objects.get(id=pk)
    print('data',data)
    context={'room':data}
    return render(request,'app/Room.html',context)

def createroom(request):
    context={}
    return render(request,'app/room_form.html',context)