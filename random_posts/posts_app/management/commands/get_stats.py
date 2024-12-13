from django.core.management.base import BaseCommand
from posts_app.models import CustomUser,Post
from django.utils.timezone import now
from django.db.models import Count
class Command(BaseCommand):
    help = "get the stats created this month"


    def handle(self, *args, **options):

        today = now()
        self.stdout.write(str(today))
        start_of_month = today.replace(day=1)
        self.stdout.write(str(start_of_month))

        user_count = CustomUser.objects.filter(date_joined__gte=start_of_month).count()
        post_count =Post.objects.filter(created_at__gte=start_of_month).count()
        user_with_highest_posts = (
            CustomUser.objects.annotate(posts=Count('user_posts'))  
            .order_by('-posts')
            .first()
        )
        self.stdout.write(self.style.SUCCESS(f"Users registered this month {user_count}"))
        self.stdout.write(self.style.SUCCESS(f"Posts created this month {post_count}"))
        self.stdout.write(self.style.NOTICE(f"User with highest number of posts {user_with_highest_posts.username}"))
        