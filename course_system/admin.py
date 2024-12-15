from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Subscription)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(UploadedFile)