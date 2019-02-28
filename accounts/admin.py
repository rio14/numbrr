from django.contrib import admin

# Register your models here.
from accounts.models import Userprofile

class User_admin(admin.ModelAdmin):
    list_display = ('owner','mobile','area','senderid')

admin.site.register(Userprofile, User_admin)
