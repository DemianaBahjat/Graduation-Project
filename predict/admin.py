from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Stroke)
admin.site.register(Diet)
admin.site.register(Stroke_Diet_Map)
admin.site.register(Live_data)