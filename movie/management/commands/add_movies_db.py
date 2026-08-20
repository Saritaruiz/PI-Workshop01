import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from movie.models import Movie


class Command(BaseCommand):
	help = 'Carga 100 peliculas desde el dataset inicial.'

	def handle(self, *args, **options):
		dataset_path = Path(__file__).with_name('movies_initial.csv')

		with dataset_path.open(encoding='utf-8', newline='') as dataset:
			movies = csv.DictReader(dataset)
			created_count = 0

			for movie_data in list(movies)[:100]:
				title = movie_data['title'].strip()[:100]
				if not title:
					continue

				defaults = {
					'description': movie_data['plot'].strip()[:250],
					'genre': movie_data['genre'].strip()[:250],
					'year': int(movie_data['year']) if movie_data['year'].isdigit() else None,
					'image': 'movie/images/default.jpg',
					'url': movie_data['poster'].strip(),
				}
				_, created = Movie.objects.update_or_create(
					title=title,
					defaults=defaults,
				)
				if created:
					created_count += 1

		self.stdout.write(
			self.style.SUCCESS(f'{created_count} peliculas creadas correctamente.')
		)
