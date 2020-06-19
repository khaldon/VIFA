from django import forms
from .models import Room
# from django.http import Http404


class RoomForm(forms.ModelForm):
    room_pass = forms.CharField(required=False)

    class Meta:
        model = Room
        fields = ('title',
                  'description',
                  'stream_time',
                  'max_viewers_amount',
                  'room_pass'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['stream_time'].widget.attrs.update({'autocomplete': 'off'})


class AuthRoomForm(forms.ModelForm):
    password2 = forms.CharField(max_length=150)

    class Meta:
        model = Room 
        fields = ('room_pass',)    
        exclude = ['room_pass']

