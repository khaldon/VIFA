from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, DeleteView
from .models import Room
from users.models import  CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import assign_perm
from django.contrib import messages
from .forms import RoomForm, AuthRoomForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

User = settings.AUTH_USER_MODEL


class RoomView(ListView):
    model = Room
    queryset = Room.objects.all()
    paginate_by = 10
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'


@login_required
def join_room(request, uuid):
    room = get_object_or_404(Room, invite_url=uuid)
    user = request.user
    room.viewer.add(user)
    return HttpResponse()


def leave_room(request,uuid):
    room = get_object_or_404(Room,invite_url=uuid)
    user = request.user
    room.viewer.remove(user)
    return redirect('rooms:rooms')


def banned_viewers(request):
    creator = get_object_or_404(CustomUser, username=request.user.username)
    creator = creator.creator_room.all()
    return render(request, 'rooms/banned_viewer.html', {'creator_room': creator})


def ban_viewer(request, uuid, user_id):
    room = get_object_or_404(Room, invite_url=uuid)
    viewer = get_object_or_404(CustomUser, id=user_id)
    if viewer in room.viewer.all():
        room.banned_viewer.add(viewer)
        room.viewer.remove(viewer)
        return redirect('rooms:viewer_banned')
    else:
        room.banned_viewer.remove(viewer)
        room.viewer.add(viewer)
        return redirect('rooms:viewer_banned')


def auth_join(request, room, uuid):
    room = get_object_or_404(Room, invite_url=uuid)
    if request.user in room.creator.all():
        return HttpResponseRedirect(Room.get_absolute_url(room))
    join_key = f"joined_{room.invite_url}"
    if request.session.get(join_key, False):
        join_room(request,uuid)
        return HttpResponseRedirect(Room.get_absolute_url(room))
    else:
        if request.method == 'POST':
            user = request.user.username
            form_auth = AuthRoomForm(request.POST)
            if form_auth.is_valid():
                try:
                    room_pass = getattr(Room.objects.get(invite_url=uuid), 'room_pass')
                except ValueError:
                    raise Http404
                password2 = form_auth.cleaned_data.get('password2')
                if room_pass != password2:
                    messages.error(request, 'Doesn\'t match')
                    return HttpResponseRedirect(request.get_full_path())
                else:
                    user = CustomUser.objects.get(username=user)
                    try:
                        room = get_object_or_404(Room, invite_url=uuid)
                    except ValueError:
                        raise Http404
                    assign_perm('pass_perm', user, room)
                    if user.has_perm('pass_perm', room):
                        request.session[join_key] = True
                        join_room(request,uuid)
                        return HttpResponseRedirect(Room.get_absolute_url(room))
                    else:
                        return HttpResponse('Problem issues')
        else:
            form_auth = AuthRoomForm()
        return render(request,'rooms/auth_join.html', {'form_auth': form_auth, 'uuid': uuid})


class CreatorCreatedRooms(LoginRequiredMixin, ListView):
    model = Room
    paginate_by = 20
    template_name = 'rooms/creator_created_rooms.html'
    context_object_name = 'creator_rooms'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.creator_room.all()


@login_required
def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST, request.FILES)
        if room_form.is_valid():
            new_room = room_form.save()
            new_room.teacher.add(request.user)
            return redirect(new_room.get_absolute_url())
    else:
        room_form = RoomForm()
    return render(request,'rooms/create_room.html', {'room_form': room_form})


def show_chat_page(request,room_name):
    room = get_object_or_404(Room,invite_url=room_name)
    return render(request,"rooms/room_detail.html",{'room_name':room_name,'room':room})
