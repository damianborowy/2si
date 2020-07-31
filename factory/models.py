from django.core.exceptions import ValidationError
from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset().order_by("type")


class Category(models.Model):
    type = models.CharField(max_length=1, choices=[(1, "BOS"), (2, "QUOS")], default=1)
    name = models.CharField(max_length=128, default="")
    color = models.CharField(max_length=1, choices=[(1, "Red"), (2, "")])
    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "Categories"

    def type_display(self):
        return self.get_type_display()

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"


class RuleManager(models.Manager):
    def get_queryset(self):
        return super(RuleManager, self).get_queryset().order_by("order")


class Rule(SortableMixin):
    name = models.CharField(max_length=128, default="")
    category = SortableForeignKey(Category, on_delete=models.CASCADE)
    order = models.IntegerField(default=-1, editable=False, db_index=True)
    is_important = models.BooleanField(default=False)
    objects = RuleManager()

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.order == -1:
            self.order = len(Rule.objects.all())
        super(Rule, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        succeeding_rules = Rule.objects.filter(order__gt=self.order)
        for rule in succeeding_rules.iterator():
            rule.order = rule.order - 1
            rule.save()
        super(Rule, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.order}. {self.name}"

    def __unicode__(self):
        return self.name


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

    def __str__(self):
        return f"{self.name} {self.surname}"


class Contribution(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.date.year}/{self.date.month}/{self.date.day} - {self.employee}"
