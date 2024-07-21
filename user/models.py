from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            # 如果是更新，删除旧的头像
            try:
                old_avatar = User.objects.get(pk=self.pk).avatar
                if old_avatar and self.avatar and old_avatar != self.avatar:
                    old_avatar.delete(save=False)
            except User.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return static('images/default-avatar.png')
