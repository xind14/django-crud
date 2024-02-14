from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.snack = Snack.objects.create(name="pizza", description='type of snack', purchaser=self.user, image_url='https://upload.wikimedia.org/wikipedia/commons/9/91/Pizza-3007395.jpg')

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "pizza")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.name}", "pizza")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(self.snack.description, 'type of snack')

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pizza")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: tester")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "name": "pizza",
                "description": "type of snack",
                "purchaser": self.user.id,
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Pizza-3007395.jpg"
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "pizza")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"name": "Updated name", "description": 'type of meal', "purchaser": self.user.id, "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Pizza-3007395.jpg"},
        )

        self.assertRedirects(
            response, reverse("snack_detail", args="1"), target_status_code=200
        )

    def test_snack_update_bad_url(self):
        response = self.client.post(
            reverse("snack_update", args="9"),
            {"name": "Updated name", "description": 'type of meal', "purchaser": self.user.id, "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Pizza-3007395.jpg"},
        )

        self.assertEqual(response.status_code, 404)

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)

    # you can also tests models directly
    def test_model(self):
        snack = Snack.objects.create(name="pizza", purchaser=self.user)
        self.assertEqual(snack.name, "pizza")