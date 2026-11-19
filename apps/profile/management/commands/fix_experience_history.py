
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.profile.models import Experience, Profile, Project


def get_experience(profile, company, job_title):
    try:
        return Experience.objects.get(
            profile=profile,
            company=company,
            job_title=job_title,
        )
    except Experience.DoesNotExist as exc:
        raise CommandError(
            f"Experience not found: {job_title} at {company}."
        ) from exc
    except Experience.MultipleObjectsReturned as exc:
        raise CommandError(
            f"Multiple experiences found: {job_title} at {company}."
        ) from exc


class Command(BaseCommand):
    help = "Correct overlapping professional experiences."

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

        # Find the contracting company experience.
        virtualmind = get_experience(
            profile,
            "Virtualmind",
            "Software Developer",
        )

        # Correct BrazilJS dates.
        braziljs = get_experience(
            profile,
            "BrazilJS",
            "Full-stack Developer",
        )
        braziljs.start_month = "2019-03"
        braziljs.end_month = "2021-03"
        braziljs.save(
            update_fields=["start_month", "end_month"]
        )

        # Correct On2 dates.
        on2 = get_experience(
            profile,
            "On2",
            "Senior Software Engineering",
        )
        on2.start_month = "2021-04"
        on2.end_month = "2022-02"
        on2.save(
            update_fields=["start_month", "end_month"]
        )

        # Convert client experiences into projects under Virtualmind.
        client_names = ["Technovation", "Reveal Markets"]

        for company in client_names:
            client_experience = get_experience(
                profile,
                company,
                "Software Developer",
            )

            Project.objects.update_or_create(
                profile=profile,
                name=company,
                defaults={
                    "experience": virtualmind,
                    "role": (
                        "Software Developer — "
                        "Virtualmind client project"
                    ),
                    "description": client_experience.description,
                    "technologies": client_experience.technologies,
                    "start_month": client_experience.start_month,
                    "end_month": client_experience.end_month,
                    "source": client_experience.source,
                    "validation_status": (
                        client_experience.validation_status
                    ),
                    "source_reference": (
                        client_experience.source_reference
                    ),
                    "validation_notes": (
                        client_experience.validation_notes
                    ),
                },
            )

            client_experience.delete()

        # Remove the self-employed experience.
        removed_count, _ = Experience.objects.filter(
            profile=profile,
            company="Self-employed",
            job_title="Full Stack Developer",
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Professional history corrected successfully."
            )
        )
        self.stdout.write(
            f"BrazilJS: {braziljs.start_month} to {braziljs.end_month}"
        )
        self.stdout.write(
            f"On2: {on2.start_month} to {on2.end_month}"
        )
        self.stdout.write(
            "Projects associated with Virtualmind: "
            "Technovation and Reveal Markets"
        )
        self.stdout.write(
            f"Self-employed records removed: {removed_count}"
        )
