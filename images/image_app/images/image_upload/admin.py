from django.contrib import admin
from .models import Image, Profile, AccountTier, Thumbnail, BinaryImage
# Register your models here.

admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(AccountTier)
admin.site.register(Thumbnail)
admin.site.register(BinaryImage)