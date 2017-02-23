from django.contrib import admin

from icebreaker_backend.models import User, Random, Picture, Contacts, Blocked


class UserAdmin(admin.ModelAdmin):
    list_display = ('enroll', 'gender', 'branch', 'college', 'batch', 'picture', 'blocked', 'contacts', 'pic_url',
                    'status')


class PictureAdmin(admin.ModelAdmin):
    list_display = 'picture'


class ContactAdmin(admin.ModelAdmin):
    list_display = 'enroll'


class BlockedAdmin(admin.ModelAdmin):
    list_display = ('enroll')


class RandomAdmin(admin.ModelAdmin):
    list_display = ('enroll', 'gender', 'time')


admin.site.register(User, UserAdmin)
admin.site.register(Picture)
admin.site.register(Contacts)
admin.site.register(Blocked)
admin.site.register(Random)
