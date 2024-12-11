from django.test import TestCase
from posts_app.form import CustomUserCreationForm,PostCreationForm,UserUpdateForm,CustomAuthenticationForm
from posts_app.models import CustomUser,Post
from django.contrib.auth import get_user_model
class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "bio": "This is a test bio.",
            "sex": "M",
            "phone_number": "123456789",
            "age": 25,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "username": "testuser",
            "password1": "password123",
            "password2": "password456",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2",form.errors)

class PostCreationFormTest(TestCase):
    def test_valid_post_form(self):
        form_data = {
            "visibility": "public",
            "categories": "Tested",
            "content": "This is a valid post content.",
        }
        form = PostCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_post_form_missing_field(self):
        form_data = {
            "visibility": "public",
            "content": "This is a valid post content.",
        }
        form = PostCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("categories", form.errors)


class AuthenticationFormTest(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create(username="testuser",
            password="password123",
        )

    def test_valid_login_form(self):
        form_data = {
            "username": "testuser",
            "password": "password123",
        }
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserUpdateFormTest(TestCase):
    def test_valid_user_update_form(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            email="testuser@example.com",
        )
        form_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "User",
            "email": "updateduser@example.com",
            "age": 30,
            "sex": "F",
            "phone_number": "987654321",
            "bio": "Updated bio.",
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form_email(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            email="testuser@example.com",
        )
        form_data = {"email": "invalid-email"}
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)