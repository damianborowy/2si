from django.contrib import admin
from factory.models import Category, Rule, Location, Settings, Employee, Contribution
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline


class RuleInline(SortableStackedInline):
    model = Rule
    extra = 1


@admin.register(Category)
class CategoryAdmin(NonSortableParentAdmin):
    inlines = [RuleInline]
    list_display = ["type_display", "name"]


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
