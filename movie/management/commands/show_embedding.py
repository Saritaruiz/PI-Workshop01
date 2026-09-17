import random
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Show the stored embedding of a random movie"

    def handle(self, *args, **kwargs):
        # ✅ Selecciona una película al azar
        movie = random.choice(list(Movie.objects.all()))

        # ✅ Recupera el array desde el campo binario
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(f"Pelicula: {movie.title}")
        self.stdout.write(f"Descripcion: {movie.description[:120]}...")
        self.stdout.write("")
        self.stdout.write(f"Embedding almacenado en la base de datos:")
        self.stdout.write(f"  dimension: {embedding_vector.shape[0]}")
        self.stdout.write(f"  bytes en BD: {len(movie.emb)}")
        self.stdout.write("")
        self.stdout.write(f"  primeros 10 valores:")
        self.stdout.write(f"  {embedding_vector[:10]}")
