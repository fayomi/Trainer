from django.contrib import admin
from .models import TrainerProfile, ClientProfile, Workout

# Register your models here.
admin.site.register(TrainerProfile)
# class TrainerProfileAdmin(admin.ModelAdmin):
#
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug':('name',)}
# admin.site.register(TrainerProfile, TrainerProfileAdmin)

admin.site.register(ClientProfile)
admin.site.register(Workout)
