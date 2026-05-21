from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.models import AssessmentPack, AssessmentVersion
from core.pack_loader import load_pack


class Command(BaseCommand):
    help = "Import an assessment pack JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "slug",
            type=str,
            help="Pack slug, for example: dating_readiness",
        )

        parser.add_argument(
            "--publish",
            action="store_true",
            help="Mark this pack version as published.",
        )

        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing pack/version records if they already exist.",
        )

    def handle(self, *args, **options):
        slug = options["slug"]
        should_publish = options["publish"]
        should_update = options["update"]

        try:
            pack = load_pack(slug)
        except FileNotFoundError as e:
            raise CommandError(str(e))
        except ValueError as e:
            raise CommandError(str(e))

        pack_slug = pack["slug"]
        version_number = pack["version"]

        if pack_slug != slug:
            raise CommandError(
                f"Slug mismatch: command slug is '{slug}', but pack.json slug is '{pack_slug}'."
            )

        pack_defaults = {
            "title": pack["title"],
            "subtitle": pack.get("subtitle", ""),
            "description": pack.get("description", ""),
            "is_active": True,
        }

        pack_obj, pack_created = AssessmentPack.objects.get_or_create(
            slug=pack_slug,
            defaults=pack_defaults,
        )

        if not pack_created and should_update:
            for field, value in pack_defaults.items():
                setattr(pack_obj, field, value)
            pack_obj.save()

        version_defaults = {
            "status": "published" if should_publish else "draft",
            "config_json": pack,
            "published_at": timezone.now() if should_publish else None,
        }

        version_obj, version_created = AssessmentVersion.objects.get_or_create(
            pack=pack_obj,
            version_number=version_number,
            defaults=version_defaults,
        )

        if not version_created and should_update:
            version_obj.status = "published" if should_publish else version_obj.status
            version_obj.config_json = pack
            if should_publish:
                version_obj.published_at = timezone.now()
            version_obj.save()

        self.stdout.write(self.style.SUCCESS("Pack import complete."))
        self.stdout.write(f"Pack: {pack_obj.slug}")
        self.stdout.write(f"Version: {version_obj.version_number}")
        self.stdout.write(f"Pack created: {pack_created}")
        self.stdout.write(f"Version created: {version_created}")
        self.stdout.write(f"Status: {version_obj.status}")