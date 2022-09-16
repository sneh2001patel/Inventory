from django.contrib import admin
from .models import Item, Area
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'quantity', 'area']
    list_filter = ['category', 'area']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('category', 'quantity', 'area')}
         ),
    )
    search_fields = ['category']
    ordering = ['category']
    filter_horizontal = ()


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    list_filter = ['name', 'location']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ()

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Area, AreaAdmin)
