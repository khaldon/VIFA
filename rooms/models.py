from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
import uuid
# Create your models here.
User = settings.AUTH_USER_MODEL


class Room(models.Model):
    creator = models.ForeignKey(User, related_name='creator_room', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(default=timezone)
    share = models.BooleanField(default=False)
    stream_time = models.TimeField()
    viewers = models.ManyToManyField(User, related_name='room_viewer', blank=True)
    banned_viewer = models.ManyToManyField(User, related_name='forbidden_viewer', blank=True)
    invite_url = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    max_viewers_amount = models.PositiveIntegerField()



    class Meta:
        ordering = ('-created',)
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('pass_perm', 'Pass permission'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rooms:room_detail', args=[str(self.invite_url)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
