from django.contrib import admin
from .models import Item, Area, Report
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ItemAdmin(admin.ModelAdmin):
    list_display = ['uid', 'code', 'quantity', 'area']
    list_filter = ['code', 'area']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('code', 'quantity', 'area')}
         ),
    )
    search_fields = ['description']
    ordering = ['description']
    filter_horizontal = ()


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    list_filter = ['name', 'location']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ()


class TestAdmin(admin.ModelAdmin):
    list_display = ['areas']
    filter_horizontal = ()


class ReportAdmin(admin.ModelAdmin):
    list_display = ['item', 'user']
    list_filter = ['user', 'date']
    search_fields = ['user']
    ordering = ['date']
    filter_horizontal = ()


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Report, ReportAdmin)
