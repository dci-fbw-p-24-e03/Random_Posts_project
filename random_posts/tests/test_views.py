from django.test import TestCase,Client
from django.urls import reverse
from posts_app.models import CustomUser,Post

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        self.post = Post.objects.create(
            user=self.user,
            content="This is a test post content",
            categories="Test Category",
            visibility="public"
        )

    def test_home_page_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts_app/home.html")

    def test_users_list_view(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts_app/users.html")
        self.assertIn(self.user,response.context["users"])

    def test_posts_list_view(self):
        response = self.client.get(reverse("posts-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_app/posts.html")
        self.assertIn(self.post, response.context["posts"])

    def test_user_detail_view(self):
        response = self.client.get(reverse("user-details", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_app/profile.html")
        self.assertEqual(response.context["user"], self.user)

    def test_post_detail_view(self):
        response = self.client.get(reverse("post-details", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_app/post_details.html")
        self.assertEqual(response.context["post"], self.post)

    def test_user_posts_view(self):
        response = self.client.get(reverse("user-posts", kwargs={"username": self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_app/user_posts.html")
        self.assertIn(self.post, response.context["posts"])

    def test_user_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts_app/register.html")

    def test_user_login_view(self):
        response = self.client.post(reverse("login"),data={"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("home"))

    def test_user_logout_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_post_create_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("new-post"),
            data={
                "content": "Another test post",
                "categories": "Test Category",
                "visibility": "public",
            }
        )
        self.assertEqual(response.status_code, 200) 
    def test_post_create_without_login(self):
        response = self.client.post(
            reverse("new-post"),
            data={
                "content": "Another test post",
                "categories": "Test Category",
                "visibility": "public",
            }
        )
        self.assertEqual(response.status_code, 302)
         
    def test_post_update_view(self):
        self.client.login(username="testuser", password="password123")
        
        response = self.client.post(
            reverse("post-update", kwargs={"pk": self.post.pk}),
            data={
                "content": "Updated content tha is longer than 20 chars",
                "categories": "Updated data",
                "visibility": "private",
            }
        )
        self.assertEqual(response.status_code,302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, "Updated content tha is longer than 20 chars")

    def test_post_delete_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("post-delete", kwargs={"pk": self.post.pk}))
        self.assertRedirects(response, reverse("user-posts", kwargs={"username": "testuser"}))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())



