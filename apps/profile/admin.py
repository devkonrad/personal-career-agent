from django.contrib import admin

from apps.profile.models import (
    Education,
    Experience,
    Language,
    Profile,
    Project,
    Skill,
)


class SourcedModelAdmin(admin.ModelAdmin):
    list_filter = ("source", "validation_status")
    list_select_related = ("profile",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "location", "updated_at")
    search_fields = ("full_name", "email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Experience)
class ExperienceAdmin(SourcedModelAdmin):
    list_display = (
        "job_title",
        "company",
        "start_month",
        "end_month",
        "validation_status",
    )
    search_fields = ("company", "job_title", "description")
    list_filter = ("source", "validation_status", "employment_type")


@admin.register(Skill)
class SkillAdmin(SourcedModelAdmin):
    list_display = ("name", "category", "validation_status")
    search_fields = ("name",)
    list_filter = ("source", "validation_status", "category")


@admin.register(Education)
class EducationAdmin(SourcedModelAdmin):
    list_display = (
        "institution",
        "qualification",
        "field_of_study",
        "validation_status",
    )
    search_fields = ("institution", "qualification", "field_of_study")


@admin.register(Language)
class LanguageAdmin(SourcedModelAdmin):
    list_display = ("name", "proficiency", "validation_status")
    search_fields = ("name",)
    list_filter = ("source", "validation_status", "proficiency")


@admin.register(Project)
class ProjectAdmin(SourcedModelAdmin):
    list_display = ("name", "role", "validation_status")
    search_fields = ("name", "description")
