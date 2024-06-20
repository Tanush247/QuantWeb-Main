from django.contrib import admin
from .models import CommonModel,UserModel
# Register your models here.

admin.site.register(CommonModel)
admin.site.register(UserModel)
