from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from posts_app.models import CustomUser,Post
import random
import faker

class Command(BaseCommand):
    help = "generate 100 fake user and 100 fake post"

    def handle(self, *args, **kwargs):

        fake = faker.Faker()
        for _ in range(100):
            username = "fake_user"+fake.user_name()
            first_name = fake.first_name()
            email = fake.email()
            phone_number = fake.phone_number()
            age = random.randint(18, 70)  # Random age between 18 and 70
            bio = fake.text(max_nb_chars=50)
            sex = random.choice(['M', 'F'])

            CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                phone_number=phone_number,
                age=age,
                sex=sex,
                password=get_random_string(length=15)  )
            self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
        
        for _ in range(100):
            user = CustomUser.objects.filter(username__startswith="fake_user").order_by("?").first()
            content = fake.text(max_nb_chars=200)
            categories = fake.word()
            visibility = random.choice(['public','private'])
            Post.objects.create(
                user=user,
                content=content,
                categories = categories,
                visibility=visibility
            )

