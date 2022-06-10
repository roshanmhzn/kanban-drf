from django.contrib import admin

from boardapi.models import Board


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
admin.site.register(Board, BoardAdmin)