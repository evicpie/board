from django.contrib import admin

from .models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'created', 'updated', 'status']
    list_editable = ['status']
    raw_id_fields = ['author']
    list_filter = ['created', 'updated', 'author']
    search_fields = ['content','created']
    ordering = ['-updated','-created']
    actions = ['status_normal', 'status_banned']

    def status_normal(self, request, queryset):
        updated_count = queryset.update(status='normal')
        self.message_user(request, '{}건의 포스팅을 정상으로 변경'.format(updated_count))
    status_normal.short_description = '지정 포스팅을 정상으로 변경'

    def status_banned(self, request, queryset):
        updated_count = queryset.update(status='banned')
        self.message_user(request, '{}건의 포스팅을 안보이게 변경'.format(updated_count))
    status_banned.short_description = '지정 포스팅을 안보이게 변경'

admin.site.register(Board, BoardAdmin)
