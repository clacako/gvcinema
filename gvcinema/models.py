from django.db import models

class Genre(models.Model):
    external_id    = models.IntegerField(blank=True)
    created         = models.DateTimeField(blank=True)
    created_by      = models.CharField(max_length=45, blank=True, null=True)
    name            = models.CharField(max_length=45, blank=True)
    description     = models.CharField(max_length=105, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Movie(models.Model):
    external_id     = models.IntegerField(blank=True)
    created         = models.DateTimeField(blank=True)
    created_by      = models.CharField(max_length=45, blank=True, null=True)
    name            = models.CharField(max_length=45, blank=True, db_index=True)
    description     = models.CharField(max_length=255, blank=True)
    imgPath         = models.CharField(max_length=105, blank=True, null=True)
    duration        = models.IntegerField(blank=True)
    genre           = models.ManyToManyField(Genre, blank=True)
    language        = models.CharField(max_length=45, blank=True)
    mpaaRating      = models.JSONField(blank=True)
    userRating      = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
