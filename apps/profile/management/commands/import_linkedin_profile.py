
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.profile.models import Experience, Profile


EXPERIENCES = [
    {
        "company": "infohelp",
        "job_title": "PHP, JavaScript and ActionScript Programmer",
        "start_month": "1999-01",
        "end_month": "2000-12",
        "description": (
            "Built a PHP and MySQL content management system, modeled "
            "website data structures, and developed web services consumed "
            "by Flash websites."
        ),
        "technologies": ["PHP", "MySQL", "JavaScript", "ActionScript", "Flash"],
    },
    {
        "company": "FAMED",
        "job_title": "Scholarship Student",
        "start_month": "2001-04",
        "end_month": "2002-08",
        "description": (
            "Developed a data collection portal for medical students "
            "using PHP and MySQL."
        ),
        "technologies": ["PHP", "MySQL"],
    },
    {
        "company": "TeHospedo",
        "job_title": "PHP & MySQL Programmer",
        "start_month": "2005-12",
        "end_month": "2006-07",
        "description": "",
        "technologies": ["PHP", "MySQL"],
    },
    {
        "company": "Rede Pampa",
        "job_title": "IT Project Manager",
        "start_month": "2009-10",
        "end_month": "2011-11",
        "description": (
            "Worked on systems for newspaper delivery and financial "
            "and logistics operations. Implemented SCRUM practices."
        ),
        "technologies": ["JavaScript", "PHP", "MySQL", "VB", "jQuery", "SCRUM"],
    },
    {
        "company": "Terra Networks",
        "job_title": "Web Development Programmer and Analyst",
        "start_month": "2011-11",
        "end_month": "2016-04",
        "description": (
            "Performed systems analysis and feasibility studies, "
            "developed web systems, improved performance, established "
            "operational and security procedures, and automated processes."
        ),
        "technologies": [
            "Ruby on Rails",
            "jQuery",
            "HTML5",
            "Python",
            "Oracle",
            "SASS",
            "JavaScript",
        ],
    },
    {
        "company": "VE3 - Supply Chain Consulting & Solutions",
        "job_title": "Development Programmer and Analyst",
        "start_month": "2016-04",
        "end_month": "2018-11",
        "description": (
            "Developed web and mobile solutions for logistics, operations, "
            "and supply chain projects. Worked with PHP frameworks and "
            "an Ionic 2 and Angular Android application."
        ),
        "technologies": [
            "PHP",
            "Zend Framework",
            "Yii",
            "Vagrant",
            "PostgreSQL",
            "jQuery",
            "HTML5",
            "Xdebug",
            "Ionic 2",
            "Angular",
        ],
    },
    {
        "company": "Vnda Ecommerce",
        "job_title": "Full-stack Developer",
        "start_month": "2018-12",
        "end_month": "2019-02",
        "description": "Maintained and developed features for a Ruby on Rails application.",
        "technologies": ["Ruby on Rails"],
    },
    {
        "company": "BrazilJS",
        "job_title": "Full-stack Developer",
        "start_month": "2019-03",
        "end_month": "2021-10",
        "description": "Developed backend and frontend solutions.",
        "technologies": [],
    },
    {
        "company": "Self-employed",
        "job_title": "Full Stack Developer",
        "start_month": "2019-09",
        "end_month": "2021-10",
        "location": "Porto Alegre, Brazil",
        "description": "",
        "technologies": [],
    },
    {
        "company": "On2",
        "job_title": "Senior Software Engineering",
        "start_month": "2021-07",
        "end_month": "2022-02",
        "description": "",
        "technologies": [],
    },
    {
        "company": "Technovation",
        "job_title": "Software Developer",
        "start_month": "2022-03",
        "end_month": "2022-08",
        "location": "Menlo Park, California, USA",
        "description": (
            "Developed features for a high-traffic e-learning platform "
            "using Ruby on Rails, Vue.js, and Tailwind CSS. Wrote unit "
            "and integration tests with RSpec."
        ),
        "technologies": [
            "Ruby on Rails",
            "Vue.js",
            "Tailwind CSS",
            "RSpec",
        ],
    },
    {
        "company": "Virtualmind",
        "job_title": "Software Developer",
        "start_month": "2022-03",
        "end_month": "2026-10",
        "location": "Argentina",
        "description": (
            "Worked in international outsourcing projects, developing "
            "production software with Python, Ruby on Rails, and JavaScript "
            "in distributed client teams."
        ),
        "technologies": ["Python", "Ruby on Rails", "JavaScript"],
    },
    {
        "company": "Reveal Markets",
        "job_title": "Software Developer",
        "start_month": "2022-09",
        "end_month": "2026-10",
        "location": "USA",
        "description": (
            "Developed backend systems, financial APIs, and integrations "
            "for trading and ticket marketplace platforms. Worked with "
            "production systems, troubleshooting, and distributed teams."
        ),
        "technologies": [
            "Python",
            "Django",
            "Django REST Framework",
            "Celery",
            "PostgreSQL",
            "Docker",
            "Redis",
            "RabbitMQ",
            "REST APIs",
            "Git",
        ],
    },
]


class Command(BaseCommand):
    help = "Import the user's professional profile and LinkedIn experience."

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

        profile, _ = Profile.objects.update_or_create(
            user=user,
            defaults={
                "full_name": "Alexandre Conrado",
                "headline": (
                    "Senior Software Engineer | Ruby on Rails, Python "
                    "& Node.js | LLM & AI Integration"
                ),
                "email": "xandee1977@gmail.com",
                "phone": "+55 51 993727450",
                "linkedin_url": "https://www.linkedin.com/in/alexandreconrado",
                "github_url": "https://github.com/devkonrad",
                "location": "Porto Alegre, Rio Grande do Sul, Brazil",
                "preferred_roles": [
                    "Senior Backend Engineer",
                    "Senior Full-Stack Engineer",
                    "AI Engineer / LLM Integration",
                    "Tech Lead",
                ],
            },
        )

        created_count = 0
        updated_count = 0

        for item in EXPERIENCES:
            experience_data = item.copy()
            company = experience_data.pop("company")
            job_title = experience_data.pop("job_title")
            start_month = experience_data.pop("start_month")

            experience_data.setdefault("location", "")
            experience_data["source"] = "linkedin"
            experience_data["validation_status"] = "pending"
            experience_data["source_reference"] = (
                "LinkedIn profile text supplied by the user"
            )

            _, created = Experience.objects.update_or_create(
                profile=profile,
                company=company,
                job_title=job_title,
                start_month=start_month,
                defaults=experience_data,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS("Profile import completed."))
        self.stdout.write(f"Profile: {profile.full_name}")
        self.stdout.write(f"Experiences created: {created_count}")
        self.stdout.write(f"Experiences updated: {updated_count}")
        self.stdout.write(f"Total experiences imported: {len(EXPERIENCES)}")
