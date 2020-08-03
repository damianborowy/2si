from adminsortable.admin import SortableAdmin
from django.contrib import admin

from factory.models import Category, Rule, Location, Settings, Employee, Contribution


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ["required_contributions", "max_selections"]

    def has_add_permission(self, request, obj=None):
        return Settings.objects.count() == 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "code"]


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ["date", "employee", "rule", "location"]


admin.site.register(Location)
admin.site.register(Category, SortableAdmin)
admin.site.register(Rule, SortableAdmin)
