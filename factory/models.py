from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=1, choices=[("B", "BOS"), ("Q", "QUOS")], default="B")
    name = models.CharField(max_length=128, default="")


class RuleManager(models.Manager):
    def get_queryset(self):
        return super(RuleManager, self).get_queryset().order_by("order")


class Rule(models.Model):
    name = models.CharField(max_length=128, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.IntegerField(default=-1)
    objects = RuleManager()

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

    def insert(self, position):
        succeeding_rules = Rule.objects.filter(order__gte=position)
        for rule in succeeding_rules.iterator():
            rule.order = rule.order + 1
            rule.save()
        self.order = position
        self.save()


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
