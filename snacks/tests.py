from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack

class ThingTests(TestCase):
    
    def test_list_page_status_code(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_page_template(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "snack_list.html")
        self.assertTemplateUsed(response, "base.html")

    def setUp(self):
        purchaser = get_user_model().objects.create(username="test", password = "uncommon")
        Snack.objects.create(name="pizza", description="type of snack",purchaser=purchaser)

    def test_list_page_context(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        snacks = response.context['object_list']
        self.assertEqual(len(snacks),1)
        self.assertEqual(snacks[0].name, "pizza")
        self.assertEqual(snacks[0].description, "type of snack")
        self.assertEqual(snacks[0].purchaser.username,"test")

