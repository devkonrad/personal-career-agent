from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


month_validator = RegexValidator(
    regex=r"^\d{4}-(0[1-9]|1[0-2])$",
    message="Use the YYYY-MM format.",
)


class SourceChoices(models.TextChoices):
    LINKEDIN = "linkedin", "LinkedIn"
    RESUME = "resume", "Resume"
    USER = "user", "User provided"
    OTHER = "other", "Other"


class ValidationChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile",
    )
    full_name = models.CharField(max_length=150)
    headline = models.CharField(max_length=255, blank=True)
    professional_summary = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)

    preferred_roles = models.JSONField(default=list, blank=True)
    preferred_work_models = models.JSONField(default=list, blank=True)
    international_salary_target = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    international_salary_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    brazilian_salary_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professional profile"
        verbose_name_plural = "Professional profiles"

    def __str__(self):
        return self.full_name


class SourcedModel(models.Model):
    source = models.CharField(
        max_length=20,
        choices=SourceChoices.choices,
        default=SourceChoices.USER,
    )
    validation_status = models.CharField(
        max_length=20,
        choices=ValidationChoices.choices,
        default=ValidationChoices.PENDING,
    )
    source_reference = models.CharField(max_length=500, blank=True)
    validation_notes = models.TextField(blank=True)

    class Meta:
        abstract = True


class Experience(SourcedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    company = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=150, blank=True)
    start_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        help_text="Use YYYY-MM, for example 2022-09.",
    )
    end_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        blank=True,
        help_text="Leave blank only when the role is ongoing.",
    )
    description = models.TextField(blank=True)
    technologies = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-start_month", "company"]
        verbose_name = "Professional experience"
        verbose_name_plural = "Professional experiences"

    def __str__(self):
        return f"{self.job_title} — {self.company}"


class Skill(SourcedModel):
    class CategoryChoices(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DATABASE = "database", "Database"
        DEVOPS = "devops", "DevOps and Cloud"
        AI = "ai", "AI and LLM"
        TESTING = "testing", "Testing"
        ARCHITECTURE = "architecture", "Architecture"
        OTHER = "other", "Other"

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER,
    )
    years_of_experience = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(60)],
    )

    class Meta:
        ordering = ["category", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "name"],
                name="unique_profile_skill",
            ),
        ]

    def __str__(self):
        return self.name


class Education(SourcedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="education",
    )
    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        blank=True,
    )
    end_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        blank=True,
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-end_month", "institution"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.institution} — {self.qualification}"


class Language(SourcedModel):
    class ProficiencyChoices(models.TextChoices):
        BASIC = "basic", "Basic"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        FLUENT = "fluent", "Fluent"
        NATIVE = "native", "Native"

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="languages",
    )
    name = models.CharField(max_length=80)
    proficiency = models.CharField(
        max_length=20,
        choices=ProficiencyChoices.choices,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "name"],
                name="unique_profile_language",
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.get_proficiency_display()}"


class Project(SourcedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    experience = models.ForeignKey(
        Experience,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_projects",
    )

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)
    url = models.URLField(blank=True)
    start_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        blank=True,
    )
    end_month = models.CharField(
        max_length=7,
        validators=[month_validator],
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
