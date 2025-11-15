from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Ensure all users have the admin role set'

    def handle(self, *args, **options):
        users_updated = 0
        for user in User.objects.all():
            if user.role != 'admin':
                user.role = 'admin'
                user.save()
                users_updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {users_updated} user(s) to have admin role')
        )
