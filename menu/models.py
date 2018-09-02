from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

TIME_NOW = timezone.now()


def valid_expiry_date(date):
    if date < TIME_NOW:
        raise ValidationError(
            "expiration date cannot be today or earlier.")


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(
        default=timezone.now)
    expiration_date = models.DateTimeField(validators=[valid_expiry_date])

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
        default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
