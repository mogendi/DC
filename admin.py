from django.contrib import admin
from .models import Post, AvailClasses, CustomUser, Comment, Resources, Assignments, AssignmentsHandedIn

admin.site.register(Post)
admin.site.register(AvailClasses)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Resources)
admin.site.register(Assignments)
admin.site.register(AssignmentsHandedIn)
