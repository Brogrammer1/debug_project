import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Ingredient, Menu, Item

time = datetime.datetime.now()
time_plus_three_days = time + datetime.timedelta(days=3)


# Create your tests here.
class ViewTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            season='summer',
            expiration_date=time_plus_three_days
        )
        self.menu2 = Menu.objects.create(
            season='summer',
            expiration_date=time
        )
        self.menu3 = Menu.objects.create(
            season='summer',
            expiration_date=time_plus_three_days
        )
        self.item = Item.objects.create(
            name='cake',
            description='round cake',
            chef_id=1

        )
        self.ingredient = Ingredient.objects.create(
            name='sugar',

        )
        self.ingredient2 = Ingredient.objects.create(
            name='flour',

        )
        self.ingredient3 = Ingredient.objects.create(
            name='eggs',

        )
        self.item.ingredients.add(self.ingredient)
        self.item.ingredients.add(self.ingredient2)
        self.item.ingredients.add(self.ingredient3)
        self.menu.items.add(self.item)

    def test_menu_list(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu.season)
        self.assertNotIn(self.menu2, resp.context['menus'])

    def test_item_list(self):
        resp = self.client.get(reverse('item_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')
        self.assertContains(resp, self.item.name)
        self.assertIn(self.item, resp.context['items'])

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.menu.season)

    def test_item_detail(self):
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.item.name)
        self.assertContains(resp, self.ingredient.name)
        self.assertContains(resp, self.ingredient2.name)
        self.assertContains(resp, self.ingredient3.name)

    def test_create_new_menu(self):
        resp = self.client.get(reverse('menu_new'))
        resp2 = self.client.post(reverse('menu_new'),
                                 {'season': "test"}
                                 )
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertContains(resp, 'Create menu')

    def test_edit_menu(self):
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertContains(resp, 'Edit menu')

    def test_edit_item(self):
        resp = self.client.get(
            reverse('item_edit', kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_edit.html')
        self.assertContains(resp, 'Edit Item')
