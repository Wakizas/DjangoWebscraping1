from django.contrib import admin
from .models import Github

# Register your models here.
class GithubAdmin(admin.ModelAdmin):
    list_display = ('githubuser', 'imagelink', 'username')

admin.site.register(Github, GithubAdmin)