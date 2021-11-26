from django.contrib import admin
from blog.models import Category,Tag,Entry,User,FileUpdate
# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title','user','visiting','created_time','modified_time']

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Entry,EntryAdmin)
admin.site.register(FileUpdate)