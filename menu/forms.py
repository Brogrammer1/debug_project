from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('created_date',)


class ChangeMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('created_date',)
        items_field = forms.ModelMultipleChoiceField(
            queryset=Item.objects.all())

        def save(self):
            signup = forms.ModelForm.save(self)
            for item in self.cleaned_data['items_field']:
                signup.item_set.add(item)


class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('chef', 'created_date')
        ingredients_field = forms.ModelMultipleChoiceField(
            queryset=Ingredient.objects.all())

        def save(self):
            signup = forms.ModelForm.save(self)
            for ingredient in self.cleaned_data['ingredients_field']:
                signup.item_set.add(ingredient)
