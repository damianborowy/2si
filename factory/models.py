from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=1, choices=[("B", "BOS"), ("Q", "QUOS")], default="B")
    name = models.CharField(max_length=128, default="")


class Rule(models.Model):
    name = models.CharField(max_length=128, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=128, default="")


class Settings(models.Model):
    required_contributions = models.IntegerField(default=20)
    max_selections = models.IntegerField(default=5)


class Employee(models.Model):
    code = models.CharField(max_length=64, default="")


class Contribution(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
