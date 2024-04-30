import json
import copy
from datetime import datetime
from django import forms
from django.db import transaction
from gvcinema.models import Genre, Movie
from _gvcinema_system.utilities.numbers import generate_alphanum 

class SearchByName(forms.Form):
    name    = forms.CharField(
        widget  = forms.TextInput(
            attrs   = {
                "class"         : "form-control form-control-lg",
                "placeholder"   : "Search movies..."
            }
        )
    )

    def clean_name(self):
        name    = self.cleaned_data.get("name")

        if not name:
            raise forms.ValidationError(
                "Must not be empty"
            )
        
        return name.strip().lower()

class SaveJsonFile(forms.Form):
    json_format = forms.JSONField(
        widget  = forms.Textarea(
            attrs   = {
                "class"         : "form-control form-control-lg",
                "placeholder"   : "Enter Json here..."
            }
        )
    )
    
    def clean_json_format(self):
        json_format = self.cleaned_data.get("json_format")
        data        = json.loads(json.dumps(json_format))

        if not json_format:
            raise forms.ValidationError(
                "Must not be empty"
            )
        
        return data
    
    def save(self):
        # Data movies
        movies_json = self.cleaned_data.get("json_format")
        
        ### SAVE GENRE ###

        # Get genre
        genre_data      = [movies.get("genre") for movies in movies_json]
        genre_list      = []
        list(map(genre_list.extend, genre_data))
        genre_clean     = list(set(genre_list))
        
        # Make sure that genre does not exists in database
        genre_save      = [genre for genre in genre_clean if not Genre.objects.filter(name=genre).exists()]
        
        # Bulking save genre
        if genre_save:
            genre_bulk_save = []
            for genre in genre_save:
                genre_bulk_save.append(
                    Genre(
                        external_id = generate_alphanum(model=Genre),
                        created     = datetime.now().replace(microsecond=0),
                        created_by  = "superadmin",
                        name        = genre
                    )
                )

            Genre.objects.bulk_create(genre_bulk_save)

        ### SAVE  MOVIES ###

        # Replace genre with genre id from database
        copy_movies_json    = copy.deepcopy(movies_json)
        movie_list          = []
       
        for movies in movies_json:
            movies["genre"] = [genre.id for genre in Genre.objects.filter(name__in=movies["genre"])]
            movie_list.append(movies)

        # Delete genre from movies json
        for movies in copy_movies_json:
            del movies["genre"]
        
        # Make sure that movies does not exists in database
        movies_save = [movie for movie in movies_json if not Movie.objects.filter(name=movie.get("name")).exists()]

        # Bulking save movies
        if movies_save:
            for movie in movies_save:
                movie["external_id"]    = generate_alphanum(model=Movie)
                movie["created"]        = datetime.now().replace(microsecond=0)
                movie["created_by"]     = "superadmin"

        Movie.objects.bulk_create([Movie(**movie) for movie in movies_save])

        ### ADD GENRE ###
        
        movies_name_genre   = [
            { "name" : movie.get("name"), "genre" : movie.get("genre") }
            for movie in movie_list
        ]

        with transaction.atomic():
            for movie in movies_name_genre:
                Movie.objects.get(name  =movie.get("name")).genre.add(*movie.get("genre"))
