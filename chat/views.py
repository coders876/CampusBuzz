from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Friend
from chat.models import Message
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.


@login_required()
def index(request):
    current_user = request.user
    try:
        friends = current_user.friends.users.all()
    except:
        Friend.make_friend(current_user, current_user)
        friends = current_user.friends.users.all()
    return render(request, 'chat/temp_messenger.html', {'user' : current_user,'friends' : friends})


@login_required()
def room(request,sender_id,receiver_id):
    current_user_id = request.user.id
    receiver = User.objects.get(id=receiver_id)
    mess = Message.objects.filter((Q(sender = request.user,receiver = receiver) | Q(sender = receiver,receiver = request.user)))
    mess = mess.order_by('created')
    if current_user_id == sender_id:
        user = User.objects.get(id = receiver_id)
        return render(request, 'chat/room1.html', {
            'message': mess,
            'receiver': receiver,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        })
    else:
        return HttpResponseNotFound("unauthorised")