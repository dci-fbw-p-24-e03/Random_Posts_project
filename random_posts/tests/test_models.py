from django.test import TestCase,override_settings
import tempfile
from posts_app.models import CustomUser,Post
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import os
@override_settings(
    STATIC_ROOT=tempfile.mkdtemp(),
    MEDIA_ROOT=tempfile.mkdtemp(),
)
class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com',
            first_name='test',
            last_name='user',
            age=25,
            bio='This is a test bio.',
            sex='M'
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(),1)
        self.assertEqual(self.user.first_name,"Test")

    def test_username_validation(self):
        self.user.username = "usr"
        with self.assertRaises(ValidationError):
            self.user.clean()

    def test_ordering_in_db(self):
        user2 =  CustomUser.objects.create_user(
            username='anotheruser',
            password='testpass123',
            email='anotheruser@example.com',
            first_name='another',
            last_name='user',
            age=30,
            bio='Another test bio.',
            sex='F'
        )
        users = list(CustomUser.objects.all())
        self.assertEqual(users[0].username,"anotheruser")
        self.assertEqual(users[1].username,"testuser")

class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            age=25,
            bio='This is a test bio.',
            sex='M'
        )
        self.image_path = 'test_image.jpg'
        image = Image.new('RGB',(500,500),'blue')
        image.save(self.image_path)
        with open(self.image_path,'rb') as img:
            self.image =SimpleUploadedFile('test_image.jpg',img.read(),content_type="image/jpeg")

        self.post = Post.objects.create(
            user=self.user,
            content='This is a test post.',
            categories='TestCategory',
            visibility='public',
            image=self.image
        )

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
            os.remove(self.post.image.path)

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(),1)
        self.assertEqual(self.post.content, 'This is a test post.')

    def test_post_ordering(self):
        post2 = Post.objects.create(
            user=self.user,
            content='Another test post.',
            categories='AnotherCategory',
            visibility='private',
        )
        posts = list(Post.objects.all())
        self.assertEqual(posts[0],post2)
        self.assertEqual(posts[1],self.post)

    def test_image_resize(self):
        img = Image.open(self.post.image.path)
        self.assertLessEqual(img.width,300)
        self.assertLessEqual(img.height,300)

    def test_post_validation(self):
        self.post.content = 'Short'
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_crud_operations(self):
        # Update
        self.post.content = 'Updated content.'
        self.post.save()
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated content.')
        # Delete
        self.post.delete()
        self.assertEqual(Post.objects.count(), 0)