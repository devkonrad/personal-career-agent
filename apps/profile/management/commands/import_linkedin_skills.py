
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.profile.models import Profile, Skill


SKILLS = [
    ("PHP", "backend"),
    ("JavaScript", "frontend"),
    ("ActionScript", "frontend"),
    ("MySQL", "database"),
    ("SCRUM", "other"),
    ("Visual Basic", "other"),
    ("jQuery", "frontend"),
    ("Ruby on Rails", "backend"),
    ("HTML5", "frontend"),
    ("Python", "backend"),
    ("Oracle", "database"),
    ("SASS", "frontend"),
    ("Zend Framework", "backend"),
    ("Yii", "backend"),
    ("Vagrant", "devops"),
    ("PostgreSQL", "database"),
    ("Xdebug", "testing"),
    ("Ionic 2", "frontend"),
    ("Angular", "frontend"),
    ("Vue.js", "frontend"),
    ("Tailwind CSS", "frontend"),
    ("RSpec", "testing"),
    ("Django", "backend"),
    ("Django REST Framework", "backend"),
    ("Celery", "backend"),
    ("Docker", "devops"),
    ("Redis", "database"),
    ("RabbitMQ", "architecture"),
    ("REST APIs", "architecture"),
    ("Git", "devops"),
]


class Command(BaseCommand):
    help = "Import technologies found in the user's LinkedIn experience."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            required=True,
            help="Django username that owns the professional profile.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options["username"]
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist as exc:
            raise CommandError(
                f"User '{username}' does not exist."
            ) from exc

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist as exc:
            raise CommandError(
                "Professional profile not found."
            ) from exc

        created_count = 0
        updated_count = 0

        for name, category in SKILLS:
            _, created = Skill.objects.update_or_create(
                profile=profile,
                name=name,
                defaults={
                    "category": category,
                    "source": "linkedin",
                    "validation_status": "pending",
                    "source_reference": (
                        "Technologies listed in the user's LinkedIn "
                        "experience descriptions"
                    ),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS("Skills import completed.")
        )
        self.stdout.write(f"Skills created: {created_count}")
        self.stdout.write(f"Skills updated: {updated_count}")
        self.stdout.write(f"Total skills processed: {len(SKILLS)}")
