import os
import numpy as np
from django.shortcuts import render
from dotenv import load_dotenv
from openai import OpenAI
from movie.models import Movie


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recommendation(request):
    prompt = request.GET.get('prompt', '').strip()
    best_movie = None
    max_similarity = None
    error = None

    if prompt:
        try:
            # ✅ Cargar la API Key
            load_dotenv('openAI.env')
            client = OpenAI(api_key=os.environ.get('openai_apikey'))

            # ✅ Generar embedding del prompt
            response = client.embeddings.create(
                input=[prompt],
                model="text-embedding-3-small"
            )
            prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

            # ✅ Recorrer la base de datos y comparar
            max_similarity = -1
            for movie in Movie.objects.all():
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                similarity = cosine_similarity(prompt_emb, movie_emb)

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_movie = movie

        except Exception as e:
            error = str(e)

    return render(request, 'recommendation.html', {
        'prompt': prompt,
        'movie': best_movie,
        'similarity': max_similarity,
        'error': error,
    })
