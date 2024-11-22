from django.db import models

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True, default=0)
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    description = models.TextField()
    original_language = models.CharField(max_length=50, null=True)
    poster_path = models.TextField(null=True)
    vote_average = models.DecimalField(max_digits=15, decimal_places=1, default=0)
    adult = models.BooleanField(default=False)


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=100)


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

