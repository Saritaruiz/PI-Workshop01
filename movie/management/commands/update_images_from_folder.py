import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database from the delivered images folder"

    def handle(self, *args, **kwargs):
        # 📁 Carpeta donde están las imágenes entregadas
        images_folder = 'media/movie/images/'

        # ✅ Verifica que la carpeta exista
        if not os.path.exists(images_folder):
            self.stderr.write(f"Folder '{images_folder}' not found.")
            return

        # 📖 Índice de los archivos disponibles en la carpeta
        available = set(os.listdir(images_folder))

        updated_count = 0
        missing_count = 0

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            # ✅ Nombre esperado del archivo: m_NOMBRE_PELICULA.png
            image_filename = f"m_{movie.title}.png"

            if image_filename in available:
                # ✅ Ruta relativa que se guarda en la base de datos
                movie.image = f"movie/images/{image_filename}"
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                missing_count += 1
                self.stderr.write(f"Image not found for: {movie.title}")

        # ✅ Resumen final
        self.stdout.write(self.style.SUCCESS(
            f"Finished updating {updated_count} movie images ({missing_count} without image)."
        ))
