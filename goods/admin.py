

from django.contrib import admin
from django.template.defaultfilters import random

from .models import *

# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'quantity','price','is_required','cat', 'time_add')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_required',)
    list_filter = ('is_required','time_add')
    search_fields = ('title','body')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'time_add' )
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Goods,GoodsAdmin)

