from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Use to load base roles to db.'

    def handle(self, *args, **options):
        if User.objects.filter(username="admin").exists():
            self.stdout.write(f"Admin is existed")
        else:
            User.objects.create_superuser(username='admin', password='123456', email='admin@admin')
            self.stdout.write(f"Admin is created")
