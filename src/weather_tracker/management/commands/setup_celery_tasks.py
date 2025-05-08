from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = "Set up Celery periodic tasks"

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        task, created = PeriodicTask.objects.update_or_create(
            name="Fetch and store temperature every 1 hour",
            defaults={
                "interval": schedule,
                "task": "weather_tracker.tasks.fetch_and_store_temperature_task",
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} periodic task: {task.name}"
            )
        )
