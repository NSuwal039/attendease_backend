from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """
    Creates groups automatically after the first database migration.
    """
    if sender.name == apps.get_app_config('courses').name:  # Replace 'myapp' with the name of your app
        Group = apps.get_model('auth', 'Group')
        print()
        groups = ['Teachers', 'Students', 'Administrators']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f'Group "{group_name}" created successfully.')
