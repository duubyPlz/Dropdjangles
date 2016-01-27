from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from timetable.models import Timetable, Class, Course, UserProfile


admin.site.register(Timetable)
admin.site.register(Class)
admin.site.register(Course)



# This will put User Profile on the first page of the admin page
# UserAdmin.list_display = ('username', 'is_active', 'date_joined', 'is_staff')
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.register(UserProfile)

# This will put User Profile inside User in the admin page
admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]
admin.site.register(User, UserProfileAdmin)