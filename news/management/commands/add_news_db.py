import csv
from datetime import datetime, time
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import News


class Command(BaseCommand):
    help = 'Carga cinco noticias desde Fake.csv.'

    def handle(self, *args, **options):
        dataset_path = Path(__file__).resolve().parents[3] / 'Fake.csv'
        created_count = 0

        with dataset_path.open(encoding='utf-8', newline='') as dataset:
            for movie in list(csv.DictReader(dataset))[:5]:
                headline = movie['title'].strip()[:200]
                date_value = datetime.strptime(
                    movie['date'],
                    '%B %d, %Y'
                ).date()
                date_value = timezone.make_aware(datetime.combine(date_value, time.min))
                _, created = News.objects.update_or_create(
                    headline=headline,
                    defaults={
                        'body': movie['text'].strip(),
                        'date': date_value,
                    },
                )
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'{created_count} noticias creadas correctamente.')
        )
