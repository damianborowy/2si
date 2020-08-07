from adminsortable.admin import SortableAdmin
from django.contrib import admin

from factory.models import Category, Rule, Location, Settings, Employee, Contribution, Vacation, fix_order


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
    list_display = ["date", "employee", "type", "rule", "location"]


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ["start_date", "end_date", "employee"]


@admin.register(Category)
class CategoryAdmin(SortableAdmin):
    list_display = ["type", "order", "name"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        fix_order()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        fix_order()

    def after_sorting(self):
        fix_order()


@admin.register(Rule)
class RuleAdmin(SortableAdmin):
    list_display = ["type", "order", "name"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        fix_order()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        fix_order()

    def after_sorting(self):
        fix_order()


admin.site.register(Location)
