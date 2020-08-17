from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from colorfield.fields import ColorField
from django.db import models


def fix_order():
    fix_categories("B")
    fix_categories("Q")


def fix_categories(cat_type):
    categories = Category.objects.filter(type=cat_type)
    rule_counter = 1
    category_counter = 1

    for category in categories:
        category.order = category_counter
        category_counter = category_counter + 1
        category.save()

        rules = category.rule_set.all()
        for rule in rules:
            rule.order = rule_counter
            rule_counter = rule_counter + 1
            rule.save()


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().order_by("type", "order")


class Category(SortableMixin):
    type = models.CharField(max_length=1, choices=[("B", "BOS"), ("Q", "QUOS")], default="B")
    name = models.CharField(max_length=256, default="")
    color = ColorField(default="#FFFFFF")
    important_rule_color = ColorField(default="#FFFFFF")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order"]

    def type_display(self):
        return self.get_type_display()

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"


class RuleManager(models.Manager):
    def get_queryset(self):
        return super(RuleManager, self).get_queryset().order_by("order")


class Rule(SortableMixin):
    name = models.CharField(max_length=1024, default="")
    category = SortableForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    is_important = models.BooleanField(default=False)
    objects = RuleManager()

    class Meta:
        ordering = ["order"]

    def type(self):
        return self.category.get_type_display()

    def __str__(self):
        return f"{self.order}. {self.name}"


class Location(models.Model):
    name = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.name


class Settings(models.Model):
    required_contributions = models.IntegerField(default=20)
    max_selections = models.IntegerField(default=5)

    class Meta:
        verbose_name_plural = "Settings"


class Employee(models.Model):
    name = models.CharField(max_length=64, default="")
    surname = models.CharField(max_length=64, default="")
    code = models.CharField(max_length=64, default="")
    role = models.CharField(max_length=1, choices=[("W", "Worker"), ("M", "Line manager")], default="W")

    def __str__(self):
        return f"{self.name} {self.surname}"


class Contribution(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.date} - {self.employee}"


class ContributionRule(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=1, choices=[("P", "Positive"), ("C", "Constructive")], default="P")


class Vacation(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} {self.start_date} - {self.end_date}"
