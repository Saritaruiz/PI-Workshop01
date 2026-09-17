import os
import base64
import requests
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate images with OpenAI and update movie image field"

    def handle(self, *args, **kwargs):
        # ✅ Load environment variables from the .env file
        load_dotenv('openAI.env')

        # ✅ Initialize the OpenAI client with the API key
        client = OpenAI(
            api_key=os.environ.get('openai_apikey'),
        )
        # ✅ Folder to save images
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        # ✅ Fetch all movies
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:
            try:
                # ✅ Call the helper function
                image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)

                # ✅ Update database
                movie.image = image_relative_path
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))

                # 🔎 Stop after the first SUCCESSFUL generation
                break

            except Exception as e:
                # Some titles are rejected by OpenAI's safety system (trademarks).
                # Skip them and try the next movie.
                self.stderr.write(f"Failed for {movie.title}: {e}")
                continue

        self.stdout.write(self.style.SUCCESS("Process finished (only first movie updated)."))

    def generate_and_download_image(self, client, movie_title, save_folder):
        """
        Generates an image using OpenAI's image model and downloads it.
        Returns the relative image path or raises an exception.
        """
        prompt = f"Movie poster of {movie_title}"

        # ✅ Generate image with OpenAI
        response = client.images.generate(
            model="gpt-image-1-mini",
            prompt=prompt,
            size="1024x1024",
            quality="low",
            n=1,
        )

        # ✅ Prepare the filename and full save path
        image_filename = f"m_{movie_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        # ✅ Get the image bytes (gpt-image-* returns base64; older models a URL)
        data = response.data[0]
        if getattr(data, 'url', None):
            image_response = requests.get(data.url)
            image_response.raise_for_status()
            content = image_response.content
        else:
            content = base64.b64decode(data.b64_json)

        with open(image_path_full, 'wb') as f:
            f.write(content)

        # ✅ Return relative path to be saved in the DB (forward slashes for URLs)
        return f'movie/images/{image_filename}'
