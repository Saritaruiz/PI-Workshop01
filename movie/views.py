from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {
        'name': 'Sara Ruizzz <3',
        'movies': movies,
        'searchTerm': searchTerm,
    })


def about(request):
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')

    # Películas por año
    years = Movie.objects.values_list(
        'year',
        flat=True
    ).distinct().order_by('year')

    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 5))

    plt.bar(
        bar_positions,
        movie_counts_by_year.values(),
        width=bar_width,
        align='center'
    )

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')

    plt.xticks(
        bar_positions,
        movie_counts_by_year.keys(),
        rotation=90
    )

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()

    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # Películas por género
    movies = Movie.objects.all()

    movie_counts_by_genre = {}

    for movie in movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()

            if first_genre:
                if first_genre in movie_counts_by_genre:
                    movie_counts_by_genre[first_genre] += 1
                else:
                    movie_counts_by_genre[first_genre] = 1

    genre_positions = range(len(movie_counts_by_genre))

    plt.figure(figsize=(10, 5))

    plt.bar(
        genre_positions,
        movie_counts_by_genre.values(),
        width=bar_width,
        align='center'
    )

    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')

    plt.xticks(
        genre_positions,
        movie_counts_by_genre.keys(),
        rotation=45,
        ha='right'
    )

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()

    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    return render(
        request,
        'statistics.html',
        {
            'graphic_year': graphic_year,
            'graphic_genre': graphic_genre
        }
    )

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(
        bar_positions,
        movie_counts_by_year.keys(),
        rotation=90
    )

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(
        request,
        'statistics.html',
        {'graphic': graphic}
    )